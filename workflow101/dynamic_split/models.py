from django.db import models
from django.conf import settings
from viewflow import jsonstore
from viewflow.workflow.models import Process


class DynamicSplitProcess(Process):
    """
    Workflow process with a dynamically generated number of splitting task.
    """

    question = jsonstore.CharField(max_length=50)
    split_count = jsonstore.IntegerField(default=0)

    class Meta:
        proxy = True


class Decision(models.Model):
    """
    Decision made on a DynamicSplitProcess.
    """

    process = models.ForeignKey(DynamicSplitProcess, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    decision = models.BooleanField(default=False)
