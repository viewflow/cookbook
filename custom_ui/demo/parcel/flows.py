from django.contrib.auth.models import User

from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView


from . import models, forms


class DeliveryFlow(Flow):
    """
    Parcel Delivery
    """
    process_class = models.DeliveryProcess

    start = flow.Start(
        CreateProcessView,
        fields=["planet", "description"],
        task_title="New Parcel"
    ).Permission(
        'parcel.add_parcel'
    ).Next(this.approve)

    approve = flow.View(
        UpdateProcessView,
        form_class=forms.ApproveForm,
        task_title="Approve"
    ).Assign(
        lambda act: User.objects.filter(is_superuser=True).order_by('?')[0]
    ).Next(this.check_approve)

    check_approve = flow.If(
        cond=lambda act: act.process.approved
    ).Then(this.delivery).Else(this.end)

    delivery = flow.View(
        UpdateProcessView,
        form_class=forms.DropStatusForm
    ).Permission(
        auto_create=True
    ).Next(this.report)

    report = flow.View(
        UpdateProcessView,
        fields=["delivery_report"]
    ).Assign(
        this.delivery.owner
    ).Next(this.end)

    end = flow.End()
