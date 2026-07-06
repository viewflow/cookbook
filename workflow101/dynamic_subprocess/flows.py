from django.utils.translation import gettext_lazy as _

from viewflow import this
from viewflow.workflow import flow, lock
from viewflow.workflow.flow.views import UpdateProcessView

from .views import StartOrderView


def order_starter(activation):
    """Owner of the human task that started the parent order process.

    A child item process is attached to the order's ``NSubprocess`` task, so
    ``activation.process.parent_task.process`` is the order; we assign each
    item's packing task back to whoever placed the order.
    """
    order = activation.process.parent_task.process
    return order.flow_class.task_class._default_manager.get(
        process=order, flow_task_type="HUMAN_START"
    ).owner


class ItemFlow(flow.Flow):
    """Fulfil a single order line item.

    Kept alive by a human ``pack`` step so the parent order's ``NSubprocess``
    stays ``STARTED`` -- which is the whole point: while it is started, more
    item processes can be attached to it.
    """

    process_title = _("Order item")
    lock_impl = lock.select_for_update_lock

    start = flow.StartSubprocess(this.seed_item).Next(this.pack)

    pack = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Annotation(
            title=_("Pack item"),
            summary_template=_("Pack {{ process.data.item.title }}"),
            result_template=_("{{ process.data.item.title }} packed"),
        )
        .Assign(order_starter)
        .Next(this.end)
    )

    end = flow.End()

    def seed_item(self, activation, item):
        activation.process.data["item"] = item


class OrderFlow(flow.Flow):
    """An order fulfilled by one child process per line item.

    ``fulfill`` is an ``NSubprocess`` that starts one ``ItemFlow`` per item in
    ``process.data['items']`` and waits for all of them. The catch it solves
    (issue #258): a customer phones back to add an item *after* the order
    started. Rather than cancel and restart, a custom "Add item" action on the
    process detail page attaches one more ``ItemFlow`` to the still-running
    ``fulfill`` task (see ``viewsets.AddOrderItemView``).
    """

    process_title = _("Order (dynamic items)")
    process_description = _(
        "Start additional NSubprocess children while the parent task is still "
        "running -- add an order line item after the order started, without "
        "cancelling it."
    )
    lock_impl = lock.select_for_update_lock

    start = (
        flow.Start(StartOrderView.as_view())
        .Annotation(title=_("New order"))
        .Next(this.fulfill)
    )

    fulfill = (
        flow.NSubprocess(ItemFlow.start, lambda process: process.data.get("items", []))
        .Annotation(title=_("Fulfil items"))
        .Next(this.end)
    )

    end = flow.End()
