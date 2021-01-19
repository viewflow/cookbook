from django.db import models
from viewflow.fields import CompositeKey


class DeviceInfo(models.Model):
    device_id = models.CharField(primary_key=True, max_length=250)

    api_version = models.CharField(max_length=250)
    manufacturer = models.CharField(max_length=250)
    model = models.CharField(max_length=250)
    os_name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'device_info'
        verbose_name = 'Device'

    def __str__(self):
        return self.device_id or 'New Device'


class Readings(models.Model):
    id = CompositeKey(columns=['device_id', 'time'])

    time = models.DateTimeField()
    device = models.ForeignKey(DeviceInfo, db_column='device_id', on_delete=models.CASCADE)

    battery_level = models.FloatField(blank=True, null=True)
    battery_status = models.CharField(max_length=250)
    battery_temperature = models.FloatField(blank=True, null=True)
    bssid = models.CharField(max_length=250)
    cpu_avg_1min = models.FloatField(blank=True, null=True)
    cpu_avg_5min = models.FloatField(blank=True, null=True)
    cpu_avg_15min = models.FloatField(blank=True, null=True)
    mem_free = models.FloatField(blank=True, null=True)
    mem_used = models.FloatField(blank=True, null=True)
    rssi = models.FloatField(blank=True, null=True)
    ssid = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'readings'
        verbose_name = 'Reading'
