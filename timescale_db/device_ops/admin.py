from django.contrib import admin
from .models import DeviceInfo, Readings


@admin.register(DeviceInfo)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'model', 'os_name', 'manufacturer')
    list_filter = ('model', 'os_name', 'manufacturer')


@admin.register(Readings)
class ReadingsAdmin(admin.ModelAdmin):
    search_fields = ['device__device_id']
    readonly_fields = ('time', 'device', )
    fieldsets = (
        (None, {'fields': ('time', 'device', 'bssid', 'rssi', 'ssid')}),
        ('Battery', {'fields': ('battery_level', 'battery_status', 'battery_temperature')}),
        ('CPU', {'fields': (('cpu_avg_1min', 'cpu_avg_5min', 'cpu_avg_15min'),)}),
        ('Memory', {'fields': (('mem_free', 'mem_used'),)}),
    )
