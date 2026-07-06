from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic

from viewflow.workflow.flow.views.mixins import (
    ProcessViewTemplateNames,
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
)
from viewflow.workflow.status import STATUS

from .forms import AddItemForm, StartOrderForm


class StartOrderView(
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
    generic.FormView,
):
    """Start an order, seeding its first line item into ``process.data``.

    The base ``Process`` has no order-specific columns, so we stash the item
    list in ``process.data`` -- items just need to be JSON-serialisable to be
    handed to each child ``ItemFlow``.
    """

    form_class = StartOrderForm
    template_filename = "start.html"
    success_message = _("Order {process} has been started.")

    def form_valid(self, form):
        process = self.request.activation.process
        process.data["items"] = [{"title": form.cleaned_data["title"]}]
        process.save()
        self.request.activation.execute()
        return super().form_valid(form)


class AddOrderItemView(ProcessViewTemplateNames, generic.FormView):
    """Attach one more ``ItemFlow`` to a still-running order.

    This is the process-detail action for issue #258. It finds the order's
    running ``NSubprocess`` task and starts an extra child on it, so the join
    now also waits for the new item. Nothing changes in the core library --
    ``start_subprocess_task.run(_parent_task=task, item=...)`` is the same call
    the node makes internally when it first fans out.
    """

    flow_class = None
    viewset = None
    form_class = AddItemForm
    template_filename = "add_item.html"

    def dispatch(self, request, *args, **kwargs):
        self.process = get_object_or_404(
            self.flow_class.process_class,
            pk=kwargs["process_pk"],
            flow_class=self.flow_class,
        )
        if not self._can_add(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def _starter(self):
        return self.process.task_set.get(flow_task_type="HUMAN_START").owner

    def _can_add(self, user):
        # the person who placed the order, or a flow manager
        return (
            user == self._starter()
            or self.flow_class.instance.has_manage_permission(user, obj=self.process)
        )

    def get_context_data(self, **kwargs):
        kwargs.setdefault("process", self.process)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        item = {"title": form.cleaned_data["title"]}
        added = False
        with self.flow_class.lock(self.process.pk), transaction.atomic():
            self.process.refresh_from_db()
            task = self.process.task_set.filter(
                flow_task_type="SUBPROCESS", status=STATUS.STARTED
            ).first()
            if task is not None:
                self.process.data.setdefault("items", []).append(item)
                self.process.save(update_fields=["data"])
                # Same call NSubprocess makes internally to fan out one child.
                task.flow_task.start_subprocess_task.run(_parent_task=task, item=item)
                added = True

        if added:
            messages.success(
                self.request,
                _("Item '%(title)s' added to the order.") % item,
                fail_silently=True,
            )
        else:
            messages.error(
                self.request,
                _("The order is no longer accepting items."),
                fail_silently=True,
            )
        return HttpResponseRedirect(
            self.flow_class.instance.reverse("process_detail", args=[self.process.pk])
        )
