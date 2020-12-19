from rest_framework import serializers
from core.models import (VaccineType, Administrator, VaccineProduct, Logistics, TxHash)

service_api_key = 'c0102049-3a5c-43f8-86ae-05c63cf615b9'
api_secret = 'baf5ce54-f8da-488d-b8e9-48092208e3e7'
wallet_address = 'tlink1kszytuezy0gndtjr6fcdgjwp6v3z028sw23ptl'
wallet_secret = 'GKzXIJ093O+D6dYYIEuy3yWAo7lurzr8Q7sim9n6qlY='

class AdministratorSerializer(serializers.ModelSerializer):
    secret_key = serializers.CharField()

    class Meta:
        model = Administrator
        fields = ('code', 'address', 'secret_key')


class LogisticsSerializer(serializers.ModelSerializer):
    unnormal = serializers.SerializerMethodField()

    class Meta:
        model = Logistics
        fields = ('pk', 'progress_type', 'lot_num', 'temp', '_from', '_to', 'unnormal')

    def get_unnormal(self, obj:Logistics):
        vaccine_type = obj.vaccine_type
        if vaccine_type.min_temp <= obj.temp and vaccine_type.max_temp >= obj.temp:
            return False

        return True


class MemoSerializer(serializers.Serializer):
    code = serializers.CharField(help_text='HGD3452')
    address = serializers.CharField(help_text='tlink1hjswfvhkqjdr5tn782c7qfmql70m0rswv59w5x')
    secret_key = serializers.CharField(help_text='j/pVgKco7R+p9Dk+jgTEQKql7VLExihrzmfcEcnv7SY=')

    vac_type = serializers.CharField(help_text='Cov_Az')
    progress_type = serializers.ChoiceField(choices=Logistics.PROCESSES)
    lot_num = serializers.CharField(help_text='F088986')
    temp = serializers.FloatField()
    _from = serializers.IntegerField()
    _to = serializers.IntegerField()
