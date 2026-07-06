from django.utils.translation import gettext_lazy as _

from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow import views

from .nodes import SnoozeView


class SnoozeFlow(flow.Flow):
    """Snooze a human task out of the inbox until a chosen time.

    Long-running steps -- "wait for the customer to confirm", "chase again next
    week" -- clutter the inbox while there is nothing to do yet. The ``review``
    task here can be snoozed by its owner: it disappears from the inbox, shows
    up under a dedicated "Snoozed" menu entry, and comes back on its own once
    the wake-up time passes. No background worker is involved -- a snoozed task
    is simply one whose ``data['snoozed']`` is still in the future (issue #219).
    """

    process_title = _("Snooze a task")
    process_description = _(
        "Shows how to add a 'snooze' action to a human task -- hiding it from "
        "the inbox until later -- entirely in application code, by extending "
        "the View node and the flow viewset. Nothing snooze-specific lives in "
        "the core library."
    )

    start = (
        flow.Start(views.CreateProcessView.as_view(fields=[]))
        .Annotation(title=_("New request"))
        .Next(this.review)
    )

    review = (
        SnoozeView(views.UpdateProcessView.as_view(fields=[]))
        .Annotation(title=_("Review"))
        # auto-assign to the process starter so the task begins owned and can
        # be snoozed straight away
        .Assign(this.start.owner)
        .Next(this.end)
    )

    end = flow.End()
