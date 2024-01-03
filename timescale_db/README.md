# TimescaleDB and Django integration sample

## Quickstart

Install timescale DB - https://docs.timescale.com/latest/getting-started/installation

Get the device ops database sample - https://docs.timescale.com/latest/tutorials/other-sample-datasets

```bash
$ git clone https://github.com/viewflow/cookbook.git

$ python3 -m venv timescale_db/venv
$ source timescale_db/venv/bin/activate

$ pip install fsm101/requirements.txt --extra-index-url=...
$ python3 timescale_db/manage.py migrate
$ python3 timescale_db/manage.py runserver
```

Navigate to http://127.0.0.1:8000

<h2>Models.py modifications</h2>

Device ops models code created by `inspectdb` Django command

```bash
    python3 timescale_db/manage.py inspectdb --database device_ops
```

- `device_id` field of DeviceInfo changed to be `primary_key=True`
- new `CompositeKey` added to the `Readings` models
- `Readings.device` field changed to be a ForeignKey

```python
class DeviceInfo(models.Model):
    device_id = models.TextField(primary_key=True)
    ...

class Readings(models.Model):
    id = CompositeKey(columns=['device_id', 'time'])

    time = models.DateTimeField()
    device = models.ForeignKey(
        DeviceInfo, db_column='device_id',
        on_delete=models.CASCADE
    )

    ...
```

## Related documentation
- [Composite FK field](http://docs.viewflow.io/orm/composite_fk.html)

## Most interesting files
- [routers.py](./config/routers.py) - DB Router to integrate demo db
- [admin.py](./device_ops/admin.py) - Plain django admin support, without any modifications
- [models.py](./device_ops/models.py) - Model definitions for the demo database
- [viewset.py](./device_ops/viewset.py) - Viewflow Material CRUD


## Query Samples

https://docs.timescale.com/latest/tutorials/other-sample-datasets#in-depth-devices

### 10 most recent battery temperature readings for charging devices

```sql
SELECT time, device_id, battery_temperature
FROM readings
WHERE battery_status = 'charging'
ORDER BY time DESC LIMIT 10;
```

```python
Readings.objects.filter(
    battery_status='charging'
).values(
    'time', 'device_id', 'battery_temperature'
).order_by(
    '-time'
)[:10]
```

### Busiest devices (1 min avg) whose battery level is below 33% and is not charging

```sql
SELECT time, readings.device_id, cpu_avg_1min,
battery_level, battery_status, device_info.model
FROM readings
JOIN device_info ON readings.device_id = device_info.device_id
WHERE battery_level < 33 AND battery_status = 'discharging'
ORDER BY cpu_avg_1min DESC, time DESC LIMIT 5;
```

```python
Readings.objects.filter(
    battery_level__lt=33,
    battery_status='discharging'
).order_by(
    '-cpu_avg_1min', '-time')
.values(
    'time', 'device_id', 'cpu_avg_1min',
    'battery_level', 'battery_status',
    'device__model'
)[:5]
```

### Devices battery level statistics by hour

```sql
SELECT date_trunc('hour', time) "hour",
min(battery_level) min_battery_level,
max(battery_level) max_battery_level
FROM readings r
WHERE r.device_id IN (
    SELECT DISTINCT device_id FROM device_info
    WHERE model = 'pinto' OR model = 'focus'
) GROUP BY "hour" ORDER BY "hour" ASC LIMIT 12;
```

```python
from django.db.models import Q, Max, Min
from django.db.models.functions import Trunc

devices = DeviceInfo.objects.filter(Q(model='pinto') | Q(model='focus'))

Readings.objects.filter(
    device_id__in=devices
).annotate(
    hour=Trunc('time', 'hour')
).order_by(
    'hour'
).values(
    'hour'
).annotate(
    min_battery_level=Min('battery_level'),
    max_battery_level=Max('battery_level')
)[:12]
```
