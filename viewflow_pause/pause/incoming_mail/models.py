from django.db import models
from viewflow.models import Process


class IncomingMailProcess(Process):
    RECIPIENT_CHOICES = (
        ('SPV', 'Supervisor'),
        ('ADM', 'Administrator'),
        ('INA', 'Incident analyst'),
    )

    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    emergency = models.BooleanField(default=False)
    recipient = models.CharField(
        blank=True, null=True, max_length=3,
        choices=RECIPIENT_CHOICES)
    approved = models.BooleanField(default=False)
