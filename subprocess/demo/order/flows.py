from django.utils.decorators import method_decorator

from viewflow import frontend, flow, lock
from viewflow.activation import STATUS
from viewflow.base import Flow, this
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from . import models, views, forms


@frontend.register
class OrderItemFlow(Flow):
    process_class = models.OrderItemProcess
    lock_impl = lock.select_for_update_lock

    start = flow.StartSubprocess(this.start_func).Next(this.reserve_item)

    reserve_item = flow.View(
        views.OrderReservationView,
        task_description="Is item reservation succeed?",
        task_result_summary="Customer is {{ process.trusted|yesno:'Trusted,Unreliable' }}"
    ).Assign(
        lambda act: act.process.parent_task.process.created_by
    ).Next(this.check_reservation)

    check_reservation = flow.If(
        cond=lambda act: act.process.item.reserved
    ).Then(this.pack_item).Else(this.end)

    pack_item = flow.View(
        UpdateProcessView,
        task_description="Pack the item",
        task_result_summary="Item packed"
    ).Assign(
        lambda act: act.process.parent_task.process.created_by
    ).Next(this.end)

    end = flow.End()

    @method_decorator(flow.flow_start_func)
    def start_func(self, activation, parent_task, item):
        activation.prepare(parent_task)
        activation.process.item = item
        activation.done()
        return activation


@frontend.register
class CustomerVerificationFlow(Flow):
    """
    Customer check
    """
    process_class = models.CustomerVerificationProcess
    lock_impl = lock.select_for_update_lock

    start = flow.StartSubprocess().Next(this.verify_customer)

    verify_customer = flow.View(
        views.CustomerVerificationView,
        task_description="Is customer trusted?",
        task_result_summary="Customer considered {{ process.trusted|yesno:'Trusted,Unreliable' }}"
    ).Assign(
        lambda act: act.process.parent_task.process.created_by
    ).Next(this.end)

    end = flow.End()


@frontend.register
class OrderFlow(Flow):
    """
    Order fulfilment

    Verify customers and send ordered items.
    """
    process_class = models.OrderProcess
    lock_impl = lock.select_for_update_lock

    start = flow.Start(
        CreateProcessView,
        form_class=forms.OrderForm
    ).Next(this.verify_customer)

    verify_customer = flow.Subprocess(
        CustomerVerificationFlow.start
    ).Next(this.check_verify)

    check_verify = flow.If(
        cond=lambda act: models.CustomerVerificationProcess.objects.get(
            parent_task__status=STATUS.DONE,
            parent_task__process=act.process
        ).trusted
    ).Then(this.prepare_items).Else(this.end)

    prepare_items = flow.NSubprocess(
        OrderItemFlow.start,
        lambda p: p.orderitem_set.all()
    ).Next(this.end)

    end = flow.End()
