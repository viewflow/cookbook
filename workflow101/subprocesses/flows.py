from viewflow import this
from viewflow.workflow import flow, lock, STATUS
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView

from . import models, views, forms


class OrderItemFlow(flow.Flow):
    lock_impl = lock.select_for_update_lock

    start = flow.StartSubprocess(this.start_func).Next(this.reserve_item)

    reserve_item = (
        flow.View(
            views.OrderReservationView.as_view(),
        )
        .Annotation(
            description="Is item reservation succeed?",
            result_template="Customer is {{ process.trusted|yesno:'Trusted,Unreliable' }}",
        )
        .Assign(
            lambda activation: activation.process.parent_task.process.coerced.created_by
        )
        .Next(this.check_reservation)
    )

    check_reservation = (
        flow.If(lambda activation: activation.process.artifact.reserved)
        .Then(this.pack_item)
        .Else(this.end)
    )

    pack_item = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Annotation(description="Pack the item", result_template="Item packed")
        .Assign(
            lambda activation: activation.process.parent_task.process.coerced.created_by
        )
        .Next(this.end)
    )

    end = flow.End()

    def start_func(self, activation, item):
        activation.process.artifact = item


class CustomerVerificationFlow(flow.Flow):
    """
    Customer check
    """

    process_class = models.CustomerVerificationProcess
    lock_impl = lock.select_for_update_lock

    start = flow.StartSubprocess().Next(this.verify_customer)

    verify_customer = (
        flow.View(views.CustomerVerificationView.as_view())
        .Annotation(
            description="Is customer trusted?",
            result_template="Customer considered {{ process.trusted|yesno:'Trusted,Unreliable' }}",
        )
        .Assign(lambda activation: activation.process.parent_task.process.created_by)
        .Next(this.end)
    )

    end = flow.End().Annotation(
        summary_template="{{ process.order_process.coerced.customer_name }} {{process.trusted|yesno:'Trusted,Rejected' }}"
    )


class OrderFlow(flow.Flow):
    """
    Order fulfillment

    Verify customers and send ordered items.
    """

    process_class = models.OrderProcess
    lock_impl = lock.select_for_update_lock

    start = flow.Start(
        CreateProcessView.as_view(form_class=forms.OrderForm),
    ).Next(this.verify_customer)

    verify_customer = flow.Subprocess(
        CustomerVerificationFlow.start,
    ).Next(this.check_verify)

    check_verify = (
        flow.If(
            lambda activation: models.CustomerVerificationProcess.objects.get(
                status=STATUS.DONE, parent_task__process=activation.process
            ).trusted
        )
        .Then(this.prepare_items)
        .Else(this.end)
    )

    prepare_items = flow.NSubprocess(
        OrderItemFlow.start, lambda p: p.orderitem_set.all()
    ).Next(this.end)

    end = flow.End().Annotation(result_template="{{ process.customer_name }}")
