from viewflow.base import this, Flow
from viewflow.contrib import celery
from viewflow.rest import flow, views

from . import models
from .tasks import send_hello_world_request


class HelloRestFlow(Flow):
    """
    Sample flow with REST interface

    This is the simple approvement demo process, where one person
    requests message send and another one approves it
    """
    process_class = models.HelloRestProcess

    summary_template = "'{{ process.text }}' message to the world"

    start = (
        flow.Start(
            views.CreateProcessView,
            fields=['text'])
        .Permission(auto_create=True)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            views.UpdateProcessView,
            fields=['approved'],
            task_description="Message approvement required",
            task_result_summary="Messsage was {{ process.approved|yesno:'Approved,Rejected' }}")
        .Permission(auto_create=True)
        .Next(this.check_approve)
    )

    check_approve = (
        flow.If(cond=lambda act: act.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        celery.Job(send_hello_world_request)
        .Next(this.end)
    )

    end = flow.End()

