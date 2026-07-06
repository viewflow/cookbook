from django.urls import NoReverseMatch, path
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from viewflow import viewprop
from viewflow.workflow.flow import views as flow_views
from viewflow.workflow.flow.viewset import FlowAppViewset

from .views import not_snoozed_q, snoozed_q


class SnoozeInboxView(flow_views.FlowInboxListView):
    """Inbox with snoozed tasks filtered out and a per-row Snooze action."""

    columns = ("task_id", "task_title", "brief", "created", "snooze")

    @viewprop
    def queryset(self):
        return super().queryset.filter(not_snoozed_q())

    def snooze(self, task):
        try:
            url = task.flow_task.reverse("snooze", args=[task.process_id, task.pk])
        except NoReverseMatch:
            return ""
        return mark_safe(f'<a href="{url}">{_("Snooze")}</a>')

    snooze.short_description = ""


class SnoozedListView(flow_views.FlowInboxListView):
    """Only the current user's currently-snoozed tasks, with a wake-up action."""

    title = _("Snoozed")
    columns = ("task_id", "task_title", "snoozed_until", "wake")

    @viewprop
    def queryset(self):
        return super().queryset.filter(snoozed_q())

    def snoozed_until(self, task):
        value = task.data.get("snoozed")
        parsed = parse_datetime(value) if value else None
        if not parsed:
            return value or ""
        return date_format(timezone.localtime(parsed), "SHORT_DATETIME_FORMAT")

    snoozed_until.short_description = _("Snoozed until")

    def wake(self, task):
        try:
            url = task.flow_task.reverse("unsnooze", args=[task.process_id, task.pk])
        except NoReverseMatch:
            return ""
        return mark_safe(f'<a href="{url}">{_("Wake up")}</a>')

    wake.short_description = ""


class SnoozeFlowViewset(FlowAppViewset):
    """A ``FlowAppViewset`` that adds the whole snooze UI on top of one flow.

    Drop-in replacement for ``FlowAppViewset`` -- it hides snoozed tasks from
    the inbox, registers a ``snoozed/`` list, and swaps in a menu template that
    shows a "Snoozed" entry next to Inbox / Queue / Archive.
    """

    menu_template_name = "snooze/snooze_menu.html"
    inbox_view_class = SnoozeInboxView

    """
    Snoozed list
    """

    snoozed_view_class = SnoozedListView

    def get_snoozed_view_kwargs(self, **kwargs):
        return self.filter_kwargs(self.snoozed_view_class, **kwargs)

    @viewprop
    def snoozed_view(self):
        return self.snoozed_view_class.as_view(**self.get_snoozed_view_kwargs())

    @property
    def snoozed_path(self):
        return path("snoozed/", self.snoozed_view, name="snoozed")

    def get_context_data(self, request):
        manager = self._flow_class.task_class._default_manager
        assigned = manager.inbox([self._flow_class], request.user)
        return {
            "user_inbox": assigned.filter(not_snoozed_q()),
            "user_queue": manager.queue([self._flow_class], request.user),
            "user_snoozed": assigned.filter(snoozed_q()),
        }
