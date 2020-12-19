from django.contrib import admin

from core.models import VaccineType, VaccineProduct, Administrator, Logistics, TxHash

# Register your models here.

@admin.register(VaccineType)
class VaccineTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VaccineType._meta.fields]


@admin.register(VaccineProduct)
class VaccineProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VaccineProduct._meta.fields]


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Administrator._meta.fields]


@admin.register(Logistics)
class LogisticsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Logistics._meta.fields]


@admin.register(TxHash)
class TxHashAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TxHash._meta.fields]
