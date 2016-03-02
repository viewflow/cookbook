import extra_views

from django import forms
from django.forms.models import modelform_factory
from django.views import generic

from viewflow import flow, views as flow_views
from material import LayoutMixin, Layout, Row, Inline

from . import models


class ItemInline(extra_views.InlineFormSet):
    model = models.OrderItem
    fields = ['title', 'quantity']


class StartView(LayoutMixin,
                flow.ManagedStartViewActivation,
                flow_views.StartActivationViewMixin,
                extra_views.NamedFormsetsMixin,
                extra_views.UpdateWithInlinesView):
    model = models.OrderProcess
    layout = Layout(
        Row('customer_name'),
        Row('customer_address'),
        Inline('Order Items', ItemInline),
    )

    def get_object(self):
        return self.process


class CustomerVerificationView(flow_views.TaskViewMixin, generic.UpdateView):
    form_class = modelform_factory(
        models.CustomerVerificationProcess,
        fields=['trusted'],
        widgets={"trusted": forms.CheckboxInput})

    def get_object(self):
        return self.activation.process


class OrderReservationView(flow_views.TaskViewMixin, generic.UpdateView):
    form_class = modelform_factory(
        models.OrderItem,
        fields=['reserved'],
        widgets={"reserved": forms.CheckboxInput})

    def get_object(self):
        return self.activation.process.item
