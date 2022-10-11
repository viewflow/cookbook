from django.db import models
from viewflow import jsonstore
from viewflow.workflow.models import Process


class HelloRestProcess(Process):
    text = jsonstore.CharField(max_length=50)
    approved = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True
