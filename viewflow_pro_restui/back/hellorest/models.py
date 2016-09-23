from viewflow.models import Process
from django.db import models


class HelloRestProcess(Process):
    text = models.CharField(max_length=250)
    approved = models.BooleanField(default=False)
