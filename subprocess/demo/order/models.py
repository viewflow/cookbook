from django.db import models
from viewflow.models import Process, Subprocess


class OrderProcess(Process):
    customer_name = models.CharField(max_length=250)
    customer_address = models.CharField(max_length=250)


class OrderItem(models.Model):
    order = models.ForeignKey(OrderProcess, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    quantity = models.IntegerField(default=1)
    reserved = models.NullBooleanField()


class CustomerVerificationProcess(Subprocess):
    trusted = models.NullBooleanField()


class OrderItemProcess(Subprocess):
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
