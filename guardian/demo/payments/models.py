from django.db import models
from viewflow.models import Process


class BillProcess(Process):
    order_department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    order_item = models.CharField(max_length=250)
    quantity = models.IntegerField()
    description = models.TextField()

    accepted = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    payment_date = models.DateField(null=True)
