from django.db import models
from viewflow import jsonstore
from viewflow.workflow.models import Process


class Department(models.Model):
    name = models.CharField(unique=True, max_length=250)
    description = models.TextField(blank=True)

    class Meta:
        permissions = (
            ('can_register_bill', 'Can register new department bill'),
            ('can_accept_bill', 'Can accept department bill'),
            ('can_sign_bill', 'Can sign department bill'),
            ('can_validate_bill', 'Can validate department bill'),
            ('can_set_bill_paydate', 'Can set payment date for department bill'),
            ('can_pay_bill', 'Can pay department bill'),
        )

    def __str__(self):
        return self.name


class Bill(models.Model):
    order_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    order_item = models.CharField(max_length=250)
    quantity = models.IntegerField()
    description = models.TextField()
    payment_date = models.DateField(null=True)


class BillProcess(Process):
    class Meta:
        proxy = True

    accepted = jsonstore.BooleanField(default=False)
    signed = jsonstore.BooleanField(default=False)
    validated = jsonstore.BooleanField(default=False)
