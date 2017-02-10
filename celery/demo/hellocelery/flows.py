from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.contrib import celery
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from .models import HelloWorldProcess
from .tasks import send_hello_world_request


@frontend.register
class HelloWorldFlow(Flow):
    process_class = HelloWorldProcess

    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        celery.Job(
            send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()
