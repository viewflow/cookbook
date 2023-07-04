from django import forms
from django.http import HttpResponseRedirect
from django.forms.models import modelform_factory
from django.views import generic
from viewflow.workflow.flow.views.mixins import TaskSuccessUrlMixin
from .models import OrderItem, CustomerVerificationProcess


class CustomerVerificationView(TaskSuccessUrlMixin, generic.UpdateView):
    template_name = "viewflow/workflow/task.html"

    form_class = modelform_factory(
        CustomerVerificationProcess,
        fields=["trusted"],
        widgets={"trusted": forms.CheckboxInput},
    )

    def get_object(self):
        return self.request.activation.process

    def form_valid(self, form):
        self.object = form.save()
        self.request.activation.execute()
        return HttpResponseRedirect(self.get_success_url())


class OrderReservationView(TaskSuccessUrlMixin, generic.UpdateView):
    template_name = "viewflow/workflow/task.html"

    form_class = modelform_factory(
        OrderItem, fields=["reserved"], widgets={"reserved": forms.CheckboxInput}
    )

    def get_object(self):
        return self.request.activation.process.artifact

    def form_valid(self, form):
        self.object = form.save()
        self.request.activation.execute()
        return HttpResponseRedirect(self.get_success_url())
