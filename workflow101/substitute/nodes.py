from viewflow.workflow import flow

from .views import SubstituteTaskView


class SubstituteView(flow.View):
    """A human task that can be delegated (substituted) to another user.

    ``flow.View`` already ships a ``reassign`` transition (gated by
    ``can_unassign`` -- the owner or a flow manager), but no view is wired to
    it by default: *who* a task may be substituted to is application-specific.
    Enabling it is a one-liner -- point ``reassign_view_class`` at a view that
    collects the target user and calls ``activation.reassign(user=...)``.
    """

    reassign_view_class = SubstituteTaskView
