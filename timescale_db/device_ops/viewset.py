from viewflow.urls import Application, ModelViewset
from .models import DeviceInfo, Readings


class DeviceModelViewset(ModelViewset):
    model = DeviceInfo
    list_columns = ('device_id', 'model', 'os_name', 'manufacturer')
    list_filter_fields = ('model', 'os_name', 'manufacturer')


class ReadingsViewset(ModelViewset):
    list_columns = ('device', 'time', 'battery_level', 'cpu_avg_15min', 'mem_free')
    list_filter_fields = ('device', )
    model = Readings


class DevicesDataApplication(Application):
    viewsets = [
        DeviceModelViewset(),
        ReadingsViewset(),
    ]
