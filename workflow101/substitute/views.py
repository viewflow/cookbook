from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.views import generic

from viewflow.workflow.flow.views.mixins import (
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
)


class SubstituteForm(forms.Form):
    """Pick the user a task should be handed over to.

    Here we simply offer every active user (minus the current owner). A real
    project would apply its own delegation rules -- an explicit
    "substitute of" table, an out-of-office flag, team membership, etc. That
    policy is exactly what viewflow keeps out of its core; only the extension
    point (a ``reassign`` view on the task node) lives there.
    """

    user = forms.ModelChoiceField(queryset=None, label=_("Substitute to"))

    def __init__(self, *args, exclude=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = get_user_model()._default_manager.filter(is_active=True)
        if exclude is not None:
            queryset = queryset.exclude(pk=exclude.pk)
        self.fields["user"].queryset = queryset


class SubstituteTaskView(
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
    generic.FormView,
):
    """Reassign the current task to a user picked in the form.

    Wired onto the task node as ``reassign_view_class`` (see ``nodes.py``); the
    node's built-in, owner/manager-gated ``reassign`` transition then surfaces
    the action button automatically on the task detail page.
    """

    form_class = SubstituteForm
    template_filename = "task_substitute.html"
    success_message = _("Task {task} has been reassigned.")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["exclude"] = self.request.activation.task.owner
        return kwargs

    def form_valid(self, form):
        self.request.activation.reassign(user=form.cleaned_data["user"])
        return super().form_valid(form)
