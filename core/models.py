from django.db import models

# Create your models here.

class VaccineType(models.Model):
    name = models.CharField(max_length=20, help_text='백신이름')
    min_temp = models.FloatField(help_text='최저온도 ex) -20~-80 중 -80')
    max_temp = models.FloatField(help_text='최고온도 ex) -20~-80 중 -20')

    def __str__(self):
        return self.name

class Administrator(models.Model):
    code = models.CharField(max_length=10, help_text='admin_code')
    address = models.TextField(blank=True)
    hashed_secret_key = models.TextField(blank=True)


class VaccineProduct(models.Model):
    vaccine = models.ForeignKey(VaccineType, on_delete=models.CASCADE)


class Logistics(models.Model):
    BEFORE = 1
    TRANSFER = 2
    STORE = 3

    PROCESSES = (
        (BEFORE, 'A'),
        (TRANSFER, 'B'),
        (STORE, 'C')
    )

    progress_type = models.IntegerField(choices=PROCESSES, default=BEFORE)
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, null=True, blank=True)
    lot_num = models.CharField(max_length=50, blank=True)
    timestamp = models.IntegerField()
    temp = models.FloatField()
    vaccine_type = models.ForeignKey(VaccineType, on_delete=models.CASCADE, null=True)
    _from = models.IntegerField()
    _to = models.IntegerField()


class TxHash(models.Model):
    logistics = models.OneToOneField(Logistics, on_delete=models.CASCADE)
    tx = models.CharField(blank=True, max_length=100)