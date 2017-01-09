from viewflow.base import this, Flow
from viewflow.rest import flow, views

from . import models


class HelloRestFlow(Flow):
    """
    Sample flow with REST interface

    This is the simple approvement demo process, where one person
    requests message send and another one approves it
    """
    process_class = models.HelloRestProcess

    summary_template = "'{{ process.text }}' message to the world"

    start = flow.Start(
        views.CreateProcessView, fields=['text']
    ).Permission(
        auto_create=True
    ).Next(this.approve)

    approve = flow.View(
        views.UpdateProcessView, fields=['approved'],
        task_description="Message approvement required",
        task_result_summary="Messsage was {{ process.approved|yesno:'Approved,Rejected' }}"
    ).Permission(
        auto_create=True
    ).Next(this.check_approve)

    check_approve = flow.If(
        cond=lambda process: process.approved
    ).Then(
        this.send
    ).Else(
        this.end
    )

    send = flow.Handler(
        this.send_message
    ).Next(this.end)

    end = flow.End()

    def send_message(self, activation):
        print(activation.process.text)
