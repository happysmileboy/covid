import datetime
import hashlib

from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import (VaccineType, Administrator, VaccineProduct, Logistics, TxHash)
from core.serializers import AdministratorSerializer, LogisticsSerializer, MemoSerializer
from core.utils.line import LineManager


admin_name = dict(
    HGD3452='홍길동',
    KST1458='김성태',
    CWH9964='최원혁',
    KMJ5976='김민주',
    SJH0285='손준혁'
)

def home(request, vaccine_type, pk):
    try:
        vaccine_type = VaccineType.objects.get(name=vaccine_type)
    except:
        return render(request, 'core/condition.html')
    logistics = Logistics.objects.filter(vaccine_type=vaccine_type, _from__lte=pk, _to__gte=pk)
    last_logistics = logistics.last()
    unnormal = False
    if logistics.exclude(temp__lte=vaccine_type.min_temp, temp__gte=vaccine_type.max_temp).exists():
        unnormal = True

    etx = dict(
        unnormal=unnormal,
        vaccine_type=vaccine_type.name,
        name=last_logistics.vaccine_type.name,
        pk=pk,
        admin_name=admin_name[last_logistics.admin.code],
        address=last_logistics.admin.address,
    )

    return render(request, 'core/condition.html', etx)


def logistics(request, vaccine_type, pk):
    try:
        vaccine_type = VaccineType.objects.get(name=vaccine_type)
    except:
        return render(request, 'core/condition.html')
    logistics = Logistics.objects.filter(vaccine_type=vaccine_type, _from__lte=pk, _to__gte=pk)

    serializer = LogisticsSerializer(logistics, many=True)

    etx = dict(logistics=serializer.data,
               vaccine_type=vaccine_type,
               vaccine_pk=pk
               )

    return render(request, 'core/logistics.html', etx)


def condition_detail(request, vaccine_type, vaccine_pk, logistics_pk):
    try:
        vaccine_type = VaccineType.objects.get(name=vaccine_type)
    except:
        return render(request, 'core/condition_detail.html')

    logistics = Logistics.objects.get(pk=logistics_pk)

    unnormal = False
    if logistics.temp < vaccine_type.min_temp or logistics.temp > vaccine_type.max_temp:
        unnormal = True

    etx = dict(
        vaccine_type=vaccine_type.name,
        code=vaccine_type.name+'_'+str(vaccine_pk),
        admin_name=admin_name[logistics.admin.code],
        TXID=logistics.txhash.tx,
        vaccine_pk=vaccine_pk,
        min_temp=vaccine_type.min_temp,
        max_temp=vaccine_type.max_temp,
        temp=logistics.temp,
        unnormal=unnormal
    )

    return render(request, 'core/condition_detail.html', etx)


class TransactionViewsets(viewsets.GenericViewSet):
    queryset = Logistics.objects.all()
    serializer_class = MemoSerializer

    @action(methods=['POST'], detail=False)
    def memo(self, request):
        serializer = MemoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            administrator = Administrator.objects.get(
                code=request.data.get('code'),
                address=request.data.get('address'),
                hashed_secret_key=request.data.get('secret_key'),
            )
        except Exception as e:
            return Response(dict(exception=f'계정관련 문제: {str(e)}'), status=status.HTTP_400_BAD_REQUEST)

        try:
            vaccine_type = VaccineType.objects.get(name=request.data.get('vac_type'))
        except Exception as e:
            return Response(dict(exception=f'백신이름 문제: {str(e)}'), status=status.HTTP_400_BAD_REQUEST)

        line_manager = LineManager()

        _from = serializer.validated_data.get('_from')
        _to = serializer.validated_data.get('_to')
        progress_type = serializer.validated_data.get('progress_type')
        temp = serializer.validated_data.get('temp')
        lot_num = serializer.validated_data.get('lot_num')
        if temp < 0:
            _temp = str(int(temp * -1 * 10)) +'Bz'
        else:
            _temp = str(int(temp * 10)) + 'Az'

        if Logistics.objects.filter(lot_num=lot_num, _from=_from, _to=_to).exists():
            parent_logistics:Logistics = Logistics.objects.filter(_from=_from, _to=_to, lot_num=lot_num).last()
            parent_data = line_manager.retrieve_memo(parent_logistics.txhash.tx)['responseData']['memo']
            parent_hash = hashlib.sha256(parent_data.encode()).hexdigest()[:10]
        else:
            parent_hash = 'genesis'

        if progress_type == 1:
            _progress_type = 'A'
        elif progress_type == 2:
            _progress_type = 'B'
        else:
            _progress_type = 'C'
        timestamp = int(datetime.datetime.utcnow().timestamp())

        memo = f'{vaccine_type.name}.{_from}.{_to}.' \
               f'{timestamp}.' \
               f'{_progress_type}.{administrator.code}.{lot_num}.{_temp}.{parent_hash}'

        res = line_manager.post_memo(memo, administrator.address, administrator.hashed_secret_key)
        tx = res['responseData']['txHash']
        new_logistics = Logistics.objects.create(
            progress_type=progress_type,
            admin=administrator,
            lot_num=lot_num,
            timestamp=timestamp,
            temp=temp,
            vaccine_type=vaccine_type,
            _from=_from,
            _to=_to
        )
        TxHash.objects.create(logistics=new_logistics, tx=tx)

        return Response(dict(memo=memo, tx=tx))