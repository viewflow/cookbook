from django import forms
from django.forms.models import modelform_factory
from django.views import generic
from viewflow.flow.views import FlowViewMixin

from .models import OrderItem, CustomerVerificationProcess


class CustomerVerificationView(FlowViewMixin, generic.UpdateView):
    form_class = modelform_factory(
        CustomerVerificationProcess,
        fields=['trusted'],
        widgets={"trusted": forms.CheckboxInput})

    def get_object(self):
        return self.activation.process


class OrderReservationView(FlowViewMixin, generic.UpdateView):
    form_class = modelform_factory(
        OrderItem,
        fields=['reserved'],
        widgets={"reserved": forms.CheckboxInput})

    def get_object(self):
        return self.activation.process.item
