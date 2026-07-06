from datetime import timedelta, timezone as dt_timezone

from django import forms
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from viewflow.workflow.flow.views.mixins import (
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
)


def to_iso(value):
    """Normalise a datetime to a fixed-width UTC ISO string.

    Stored in ``task.data['snoozed']``. Fixed width + always UTC means plain
    JSON text comparison in the database (``data__snoozed__gt``) sorts
    chronologically, so we can filter snoozed tasks in the query itself -- no
    extra model field, no migration.
    """
    return value.astimezone(dt_timezone.utc).isoformat(timespec="seconds")


def now_iso():
    return to_iso(timezone.now())


def snoozed_q():
    """Tasks currently snoozed (wake-up time still in the future)."""
    return Q(data__snoozed__gt=now_iso())


def not_snoozed_q():
    """Tasks visible in the inbox: never snoozed, or the wake-up time passed.

    Spelled out as an inclusive filter rather than ``.exclude(snoozed_q())`` on
    purpose -- ``data__snoozed`` is SQL NULL for a task that was never snoozed,
    and ``NOT (NULL > now)`` is NULL, not TRUE, so an ``exclude`` would wrongly
    hide every un-snoozed task.
    """
    return Q(data__snoozed__isnull=True) | Q(data__snoozed__lte=now_iso())


# preset -> (label, how far from now). Kept tiny on purpose; a real project
# could offer a datetime picker, "after the weekend", business-hours math, etc.
PRESETS = {
    "1h": (_("In 1 hour"), timedelta(hours=1)),
    "1d": (_("Tomorrow"), timedelta(days=1)),
    "1w": (_("Next week"), timedelta(weeks=1)),
}


class SnoozeForm(forms.Form):
    until = forms.ChoiceField(
        label=_("Snooze until"),
        choices=[(key, label) for key, (label, _delta) in PRESETS.items()],
    )

    def snoozed_until(self):
        _label, delta = PRESETS[self.cleaned_data["until"]]
        return timezone.now() + delta


class SnoozeTaskView(
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
    generic.FormView,
):
    """Stash a wake-up time on the task and drop it out of the inbox.

    Snoozing changes nothing about the flow state (the task stays ``ASSIGNED``
    to the same owner) -- it only writes ``task.data['snoozed']``. The custom
    inbox query hides the task until that moment passes, then it reappears on
    its own. No timer, no background worker (see issue #219).
    """

    form_class = SnoozeForm
    template_filename = "task_snooze.html"
    success_message = _("Task {task} has been snoozed.")

    def form_valid(self, form):
        task = self.request.activation.task
        task.data["snoozed"] = to_iso(form.snoozed_until())
        task.save(update_fields=["data"])
        return super().form_valid(form)


class UnsnoozeTaskView(
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
    generic.FormView,
):
    """Clear the wake-up time so the task returns to the inbox immediately."""

    form_class = forms.Form
    template_filename = "task_unsnooze.html"
    success_message = _("Task {task} is back in your inbox.")

    def form_valid(self, form):
        task = self.request.activation.task
        task.data.pop("snoozed", None)
        task.save(update_fields=["data"])
        return super().form_valid(form)
