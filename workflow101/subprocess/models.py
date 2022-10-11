from django.db import models
from viewflow import jsonstore
from viewflow.workflow.models import Process


class OrderProcess(Process):
    class Meta:
        proxy = True

    customer_name = jsonstore.CharField(max_length=250)
    customer_address = jsonstore.CharField(max_length=250)

    @property
    def created_by(self):
        """Lookup for the owner of the task that started the flow."""
        return self.flow_class.task_class._default_manager.get(
            process=self, flow_task_type="HUMAN_START"
        ).owner


class CustomerVerificationProcess(Process):
    class Meta:
        proxy = True

    trusted = jsonstore.BooleanField(null=True)


class OrderItemProcess(Process):
    class Meta:
        proxy = True


class OrderItem(models.Model):
    order = models.ForeignKey(OrderProcess, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    quantity = models.IntegerField(default=1)
    reserved = models.BooleanField(null=True)
