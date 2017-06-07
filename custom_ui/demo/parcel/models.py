from django.db import models
from viewflow.models import Process


class DeliveryProcess(Process):
    planet = models.CharField(max_length=250)
    description = models.TextField()
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True)
    drop_status = models.CharField(
        null=True, max_length=3, default=None,
        choices=(('SCF', 'Successful'),
                 ('ERR', 'Unsuccessful'))
    )
    delivery_report = models.TextField(null=True)
