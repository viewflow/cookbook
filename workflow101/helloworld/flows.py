from django.utils.translation import gettext_lazy as _

from viewflow import this
from viewflow.contrib import celery
from viewflow.workflow import flow, lock, act
from viewflow.workflow.flow import views

from .models import HelloWorldProcess
from .tasks import send_hello_world_request


class HelloWorldFlow(flow.Flow):
    """
    Flow for sending hello world message requests.

    This process demonstrates a flow for sending hello world message requests
    that require supervisor approval before being sent.
    """

    process_class = HelloWorldProcess
    process_title = _("Hello world")
    process_description = _(
        "This process enables the user to send a message to the world, and request approval from a supervisor."
    )
    process_summary_template = _("Send '{{ process.text }}' message to the world")
    process_result_template = _(
        "{% if process.approved %}"
        "Successfully sent '{{ process.text }}' message to the world"
        "{% else %}Message was rejected"
        "{% endif %}"
    )

    lock_impl = lock.select_for_update_lock

    start = (
        flow.Start(views.CreateProcessView.as_view(fields=["text"]))
        .Annotation(title=_("New message"))
        .Permission(auto_create=True)
        .Next(this.approve)
    )

    approve = (
        flow.View(views.UpdateProcessView.as_view(fields=["approved"]))
        .Annotation(
            title=_("Approve"),
            description=_("Supervisor approvement"),
            summary_template=_("Message review required"),
            result_template=_(
                "Message was {{ process.approved|yesno:'Approved,Rejected' }}"
            ),
        )
        .Permission(auto_create=True)
        .Next(this.check_approve)
    )

    check_approve = (
        flow.If(act.process.approved)
        .Annotation(title=_("Approvement check"))
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        celery.Job(send_hello_world_request)
        .Annotation(title=_("Send message"))
        .Next(this.end)
    )

    end = flow.End().Annotation(
        title=_("End"),
        summary_template=(
            "{% load i18n %}{% if process.approved %}{% trans 'Completed' %}{% else %}{% trans 'Rejected'%}{% endif %}"
        ),
    )
