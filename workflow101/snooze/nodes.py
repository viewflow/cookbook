from django.urls import path

from viewflow import viewprop
from viewflow.workflow import flow
from viewflow.workflow.flow import utils

from .views import SnoozeTaskView, UnsnoozeTaskView


class SnoozeView(flow.View):
    """A human task whose owner can 'snooze' it out of the inbox until later.

    ``flow.View`` has no snooze concept -- snoozing is pure UI/queue policy, so
    it is kept out of the core library. Here we extend the node with two
    task-scoped URLs, ``snooze`` and ``unsnooze``, both gated by
    ``can_unassign`` (the task owner or a flow manager). The wake-up time is
    stored in ``task.data['snoozed']`` by the views; a custom viewset
    (``SnoozeFlowViewset``) hides snoozed tasks from the inbox and lists them
    under a separate "Snoozed" menu entry.

    Because the whole feature lives in this cookbook subclass, flows that don't
    use ``SnoozeView`` never grow a snooze action or a Snoozed menu item.
    """

    snooze_view_class = SnoozeTaskView
    unsnooze_view_class = UnsnoozeTaskView

    @viewprop
    def snooze_view(self):
        """View to snooze a task."""
        if self.snooze_view_class:
            return self.snooze_view_class.as_view()

    @property
    def snooze_path(self):
        if self.snooze_view:
            return path(
                f"<int:process_pk>/{self.name}/<int:task_pk>/snooze/",
                utils.wrap_task_view(
                    self, self.snooze_view, permission=self.can_unassign
                ),
                name="snooze",
            )

    @viewprop
    def unsnooze_view(self):
        """View to bring a snoozed task back to the inbox."""
        if self.unsnooze_view_class:
            return self.unsnooze_view_class.as_view()

    @property
    def unsnooze_path(self):
        if self.unsnooze_view:
            return path(
                f"<int:process_pk>/{self.name}/<int:task_pk>/unsnooze/",
                utils.wrap_task_view(
                    self, self.unsnooze_view, permission=self.can_unassign
                ),
                name="unsnooze",
            )
