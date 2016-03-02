from django.db import models
from viewflow.models import AbstractProcess, AbstractTask

from . import managers


class Planet(models.Model):
    name = models.CharField(max_length=150)
    distance = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ('land_on_planet', 'Can land on planet')
        ]


class Parcel(models.Model):
    planet = models.ForeignKey(Planet)
    description = models.TextField()


class ShipmentProcess(AbstractProcess):
    parcel = models.ForeignKey(Parcel)
    approved = models.BooleanField(default=False)
    deliver_report = models.TextField(null=True)


class ShipmentTask(AbstractTask):
    process = models.ForeignKey(ShipmentProcess)
    owner = models.ForeignKey('users.User', blank=True, null=True)
    owner_permission = models.CharField(max_length=50, blank=True, null=True)

    objects = managers.TaskManager()


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(ShipmentProcess)
    name = models.CharField(max_length=250)
    quantity = models.IntegerField(default=1)
