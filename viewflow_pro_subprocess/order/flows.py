from viewflow import flow, lock, views as flow_views
from viewflow.activation import STATUS
from viewflow.base import Flow, this
from viewflow.frontend.modules import Viewflow

from . import models, views


class OrderItemFlow(Flow):
    process_cls = models.OrderItemProcess
    lock_impl = lock.select_for_update_lock

    start = flow.StartSubprocess().Next(this.reserve_item)

    reserve_item = flow.View(
        views.OrderReservationView,
        task_description="Is item reservation succeed?",
        task_result_summary="Customer is {{ process.trusted|yesno:'Truested,Unrelaible' }}"
    ).Assign(
        lambda process: process.parent_task.process.created_by
    ).Next(this.check_reservation)

    check_reservation = flow.If(
        cond=lambda p: p.item.reserved
    ).OnTrue(this.pack_item).OnFalse(this.end)

    pack_item = flow.View(
        flow_views.ProcessView,
        task_description="Pack the item",
        task_result_summary="Item packed"
    ).Assign(
        lambda process: process.parent_task.process.created_by
    ).Next(this.end)

    end = flow.End()

    def start_func(self, activation, parent_task, item):
        activation.prepare(parent_task)
        activation.process.item = item
        activation.done()
        return activation


class CustomerVerificationFlow(Flow):
    """
    Customer check
    """
    process_cls = models.CustomerVerificationProcess
    lock_impl = lock.select_for_update_lock

    start = flow.StartSubprocess().Next(this.verify_customer)

    verify_customer = flow.View(
        views.CustomerVerificationView,
        task_description="Is customer trusted?",
        task_result_summary="Customer considered {{ process.trusted|yesno:'Trusted,Unrelaible' }}"
    ).Assign(
        lambda process: process.parent_task.process.created_by
    ).Next(this.end)

    end = flow.End()


class OrderFlow(Flow):
    """
    Order fulfitment

    Verify customers and send ordered items.
    """
    process_cls = models.OrderProcess
    lock_impl = lock.select_for_update_lock

    start = flow.Start(views.StartView) \
        .Next(this.verify_customer)

    verify_customer = flow.Subprocess(
        CustomerVerificationFlow.start
    ).Next(this.check_verify)

    check_verify = flow.If(
        cond=lambda process: models.CustomerVerificationProcess.objects.get(
            parent_task__status=STATUS.DONE,
            parent_task__process=process
        ).trusted
    ).OnTrue(this.prepare_items).OnFalse(this.end)

    prepare_items = flow.NSubprocess(
        OrderItemFlow.start,
        lambda p: p.orderitem_set.all()
    ).Next(this.end)

    end = flow.End()


Viewflow.instance.register(OrderFlow)
Viewflow.instance.register(OrderItemFlow)
Viewflow.instance.register(CustomerVerificationFlow)
