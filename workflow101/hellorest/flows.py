from viewflow import this
from viewflow.workflow import act, rest, flow
from viewflow.workflow.rest import views
from viewflow.contrib import celery

from . import models, tasks


class HelloRestFlow(flow.Flow):
    """
    Hello, world - REST example.

    This sample demonstrates pure rest flow
    """

    process_class = models.HelloRestProcess
    process_title = "Hello Rest World"
    process_goal_template = "'{{ process.text }}' message to the world"

    start = (
        rest.Start(views.CreateProcessView.as_view(fields=["text"]))
        .Permission(auto_create=True)
        .Next(this.approve)
    )

    approve = (
        rest.View(
            views.UpdateProcessView.as_view(fields=["approved"])
        )
        .Annotation(
            title="Message approvement required",
            result_template="Messsage was {{ process.approved|yesno:'Approved,Rejected' }}",
        )
        .Permission(auto_create=True)
        .Next(this.check_approve)
    )

    check_approve = (
        rest.If(cond=act.process.approved).Then(this.send).Else(this.end)
    )

    send = celery.RJob(tasks.send_hello_world_request).Next(this.end)

    end = rest.End()
