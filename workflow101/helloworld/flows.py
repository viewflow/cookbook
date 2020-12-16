from django.utils.translation import ugettext_lazy as _

from viewflow import this
from viewflow.contrib import celery
from viewflow.workflow import flow, lock, act
from viewflow.workflow.flow import views

from .models import HelloWorldProcess
from .tasks import send_hello_world_request


class HelloWorldFlow(flow.Flow):
    """
    Hello world

    This process demonstrates hello world approval request flow.
    """
    process_class = HelloWorldProcess
    process_title = _('Hello world')
    process_detail = _('This process demonstrates hello world approval request flow.')

    lock_impl = lock.select_for_update_lock

    summary_template = _("Send '{{ process.text }}' message to the world")

    start = (
        flow.Start(
            views.CreateProcessView.as_view(
                fields=['text']
            )
        )
        .Description(title=_('New message'))
        .Permission(auto_create=True)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            views.UpdateProcessView.as_view(
                fields=['approved']
            )
        )
        .Description(
            title=_('Approve'),
            detail=_("'{{ process.text }}' approvement required"),
            result=_("Messsage was {{ process.approved|yesno:'Approved,Rejected' }}")
        )
        .Permission(auto_create=True)
        .Next(this.check_approve)
    )

    check_approve = (
        flow.If(act.process.approved)
        .Description(
            title=_('Approvement check')
        )
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        celery.Job(send_hello_world_request)
        .Description(title=_('Send message'))
        .Next(this.end)
    )

    end = flow.End().Description(title=_('End'))
