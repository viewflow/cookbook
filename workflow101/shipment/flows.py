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
        .Annotation(
            title=_("Select carrier"),
            description=_(
                "Selection of a shipping carrier based on order specifics and requirements."
            ),
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
        .Annotation(
            title=_("Obtain carrier quotes"),
            description=_(
                "Gathers quotes from potential carriers to compare rates and services."
            ),
        )
        .Assign(lambda act: act.process.created_by)
        .Next(this.join_clerk_warehouse)
    )

    check_insurance = (
        flow.View(views.ShipmentView.as_view(fields=["need_insurance"]))
        .Annotation(
            title=_("Assess insurance needs"),
            description=_(
                "Determines if the shipment requires additional insurance coverage based on value and risk."
            ),
        )
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
        .Annotation(
            title=_("Complete post label"),
            description=_(
                "Fills out the postal label with the necessary details for shipping."
            ),
        )
        .Assign(act.process.created_by)
        .Next(this.join_on_insurance)
    )

    join_on_insurance = flow.Join().Next(this.join_clerk_warehouse)

    # Logistic manager
    take_extra_insurance = (
        flow.View(views.InsuranceView.as_view())
        .Annotation(
            title=_("Opt for extra insurance"),
            description=_(
                "Considers additional insurance based on the shipment's assessed needs."
            ),
        )
        .Permission("shipment.can_take_extra_insurance")
        .Next(this.join_on_insurance)
    )

    # Warehouse worker
    package_goods = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Annotation(
            title=_("Packaging"),
            description=_(
                "Ensures goods are properly packaged for safe and secure delivery."
            ),
        )
        .Permission("shipment.can_package_goods")
        .Next(this.join_clerk_warehouse)
    )

    join_clerk_warehouse = flow.Join().Next(this.move_package)

    move_package = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Annotation(
            title=_("Finalize shipment"),
            description=_(
                "Prepares the packaged goods for dispatch to the destination."
            ),
        )
        .Assign(this.package_goods.owner)
        .Next(this.end)
    )

    end = flow.End()
