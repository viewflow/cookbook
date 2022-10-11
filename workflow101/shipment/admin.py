from django.contrib import admin

from . import models


class CarrierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_default']


class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'cost']


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['shipment_no', 'carrier', 'carrier_quote', 'insurance', 'package_tag']


admin.site.register(models.Carrier, CarrierAdmin)
admin.site.register(models.Insurance, InsuranceAdmin)
admin.site.register(models.Shipment, ShipmentAdmin)
