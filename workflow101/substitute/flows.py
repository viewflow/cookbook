from django.utils.translation import gettext_lazy as _

from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow import views

from .nodes import SubstituteView


class SubstituteFlow(flow.Flow):
    """Delegate / substitute a human task to another user.

    The ``approve`` task is auto-assigned to whoever starts the process. From
    the task detail page the owner (or a flow manager) can:

    * **Unassign** it -- the built-in action returns the task to the queue so
      any other user can grab it. This alone already covers the simplest
      "cover for me" case, no custom code needed.
    * **Reassign** it -- the action added by this sample, handing the task
      directly to a specific user chosen in a custom view (``SubstituteView``).
    """

    process_title = _("Substitute / Delegate")
    process_description = _(
        "Shows how to add a 'substitute' action to a human task by extending "
        "the View node with a custom view -- reassigning the task to another "
        "user. Client delegation logic can be much more involved; here we just "
        "list all users."
    )

    start = (
        flow.Start(views.CreateProcessView.as_view(fields=[]))
        .Annotation(title=_("New request"))
        .Next(this.approve)
    )

    approve = (
        SubstituteView(views.UpdateProcessView.as_view(fields=[]))
        .Annotation(title=_("Approve"))
        # auto-assign to the process starter so the task begins owned
        .Assign(this.start.owner)
        .Next(this.end)
    )

    end = flow.End()
