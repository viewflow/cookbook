from viewflow import flow, lock
from viewflow.base import this, Flow
from django.contrib.auth import get_user_model

from . import models, views


class ShipmentFlow(Flow):
    """
    Parcel Shipment

    This process demonstrates hello world approval request flow.
    """
    process_cls = models.ShipmentProcess
    task_cls = models.ShipmentTask
    lock_impl = lock.select_for_update_lock

    start = flow.Start(views.register_shipment) \
        .Permission('parcel.add_parcel') \
        .Next(this.approve)

    approve = flow.View(views.approve_shipment) \
        .Assign(lambda p: get_user_model().objects.get(email='hubert@farnsworth.com')) \
        .Next(this.check_approve)

    check_approve = flow.If(cond=lambda p: p.approved) \
        .OnTrue(this.deliver) \
        .OnFalse(this.end)

    deliver = flow.View(views.deliver, assign_view=views.deliver_assign) \
        .Permission('parcel.land_on_planet', obj=lambda p: p.parcel.planet) \
        .Next(this.report)

    report = flow.View(views.deliver_report) \
        .Assign(this.deliver.owner) \
        .Next(this.end)

    end = flow.End()
