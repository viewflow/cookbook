from django.utils.translation import gettext_lazy as _

from viewflow import this
from viewflow.workflow import flow, lock, act
from viewflow.workflow.flow.views import UpdateProcessView

from . import models, views


class ShipmentFlow(flow.Flow):
    """
    Order Shipment

    Shipment workflow for e-commerce store back-office automation
    """

    process_class = models.ShipmentProcess
    process_title = _("Order shipment")
    process_description = _(
        "Split and synchronize work for a Manager, Clerk and Warehouse worker"
    )
    process_summary_template = """
        Shipment {{ process.artifact.shipmentitem_set.count }} items
        to {{ process.shipment.first_name }} {{ process.shipment.last_name }} / {{ process.shipment.city }}
    """

    lock_impl = lock.select_for_update_lock

    start = (
        flow.Start(views.StartView.as_view())
        .Annotation(title=_("New shipment"))
        .Permission("shipment.can_start_request")
        .Next(this.split_clerk_warehouse)
    )

    # clerk
    split_clerk_warehouse = (
        flow.Split().Next(this.shipment_type).Next(this.package_goods)
    )

    shipment_type = (
        flow.View(
            views.ShipmentView.as_view(fields=["carrier"]),
            task_description="Carrier selection",
        )
        .Assign(act.process.created_by)
        .Next(this.delivery_mode)
    )

    delivery_mode = (
        flow.If(act.process.is_normal_post)
        .Then(this.check_insurance)
        .Else(this.request_quotes)
    )

    request_quotes = (
        flow.View(views.ShipmentView.as_view(fields=["carrier_quote"]))
        .Assign(lambda act: act.process.created_by)
        .Next(this.join_clerk_warehouse)
    )

    check_insurance = (
        flow.View(views.ShipmentView.as_view(fields=["need_insurance"]))
        .Assign(act.process.created_by)
        .Next(this.split_on_insurance)
    )

    split_on_insurance = (
        flow.Split()
        .Next(this.take_extra_insurance, case=act.process.need_extra_insurance)
        .Next(this.fill_post_label)
    )

    fill_post_label = (
        flow.View(views.ShipmentView.as_view(fields=["post_label"]))
        .Assign(act.process.created_by)
        .Next(this.join_on_insurance)
    )

    join_on_insurance = flow.Join().Next(this.join_clerk_warehouse)

    # Logistic manager
    take_extra_insurance = (
        flow.View(views.InsuranceView.as_view())
        .Permission("shipment.can_take_extra_insurance")
        .Next(this.join_on_insurance)
    )

    # Warehouse worker
    package_goods = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Permission("shipment.can_package_goods")
        .Next(this.join_clerk_warehouse)
    )

    join_clerk_warehouse = flow.Join().Next(this.move_package)

    move_package = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Assign(this.package_goods.owner)
        .Next(this.end)
    )

    end = flow.End()
