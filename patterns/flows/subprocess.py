"""
Pattern:
    A call activity runs another flow as a child process and waits for it to
    finish before continuing. If the child ends with an error, the parent's
    error boundary on the call activity catches it.

Example:
    Order fulfilment calls a self-contained fulfilment subprocess. If the
    subprocess runs out of stock it ends with an "out-of-stock" error, which
    the parent catches and turns into a back-order.

Purpose:
    ``flow.Subprocess(Child.start)`` is the BPMN call activity. It keeps a
    reusable child flow independent while composing it into a parent. Pairing
    it with ``.OnError(this.recover, code=...)`` shows how a child
    ``flow.ErrorEnd("code")`` propagates a business error up to the parent.
"""

from datetime import timedelta

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from viewflow import this, jsonstore
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView
from viewflow.workflow.models import Process, Task
from viewflow.workflow.status import STATUS
from viewflow.workflow.timers import fire_due_timers


class FulfillmentProcess(Process):
    out_of_stock = jsonstore.BooleanField(
        default=False, choices=((1, "Out of stock"), (0, "In stock"))
    )

    class Meta:
        proxy = True


class FulfillmentChildProcess(Process):
    class Meta:
        proxy = True


class FulfillmentChild(flow.Flow):
    process_class = FulfillmentChildProcess

    start = flow.StartHandle(this.pick_items).Next(this.reserve)

    # the reservation runs asynchronously, so the child resolves in its own
    # transaction and a child error end can propagate up to the parent
    reserve = (
        flow.Timer(timedelta(seconds=5))
        .Annotation(title="Reserve")
        .Next(this.check_stock)
    )

    check_stock = (
        flow.BusinessRule(this.do_check_stock)
        .Annotation(title="Check Stock")
        .Next(this.route)
    )

    route = (
        flow.If(lambda a: a.process.data.get("in_stock"))
        .Then(this.pack)
        .Else(this.out_of_stock)
    )

    pack = flow.Function(this.do_pack).Annotation(title="Pack Items").Next(this.done)
    done = flow.End()

    out_of_stock = flow.ErrorEnd("out-of-stock").Annotation(title="Out of Stock")

    def pick_items(self, activation):
        # inherit the scenario flag from the calling process
        parent = activation.process.parent_task.process
        parent = FulfillmentProcess.objects.get(pk=parent.pk)
        activation.process.data["requested_out_of_stock"] = bool(parent.out_of_stock)
        activation.process.save()

    def do_check_stock(self, activation):
        activation.process.data["in_stock"] = not activation.process.data[
            "requested_out_of_stock"
        ]
        activation.process.save()

    def do_pack(self, activation):
        activation.process.data["packed"] = True
        activation.process.save()

    process_description = (
        "Reusable fulfilment subprocess: check stock, then pack or fail."
    )

    def __str__(self) -> str:
        return "A reusable child flow that packs an order or ends with an out-of-stock error."


class OrderForm(forms.ModelForm):
    class Meta:
        model = FulfillmentProcess
        fields = ["out_of_stock"]
        widgets = {"out_of_stock": forms.RadioSelect()}


class OrderFulfillment(flow.Flow):
    process_class = FulfillmentProcess

    start = (
        flow.Start(CreateProcessView.as_view(form_class=OrderForm))
        .Annotation(title="Place Order")
        .Permission(auto_create=True)
        .Next(this.fulfill)
    )

    fulfill = (
        flow.Subprocess(FulfillmentChild.start)
        .Annotation(title="Fulfil Order")
        .OnError(this.backorder, code="out-of-stock", title="Out of Stock")
        .Next(this.confirm)
    )

    confirm = (
        flow.SendHandle(this.do_confirm)
        .Annotation(title="Confirm Shipment")
        .Next(this.end)
    )

    backorder = (
        flow.Function(this.do_backorder)
        .Annotation(title="Create Back-order")
        .Next(this.end)
    )

    end = flow.End()

    def do_confirm(self, activation):
        activation.process.data["shipped"] = True
        activation.process.save()

    def do_backorder(self, activation):
        activation.process.data["backordered"] = True
        activation.process.save()

    process_description = (
        "The order calls a fulfilment subprocess; if it ends out-of-stock the "
        "error boundary turns the order into a back-order."
    )

    def __str__(self) -> str:
        return (
            "A call activity runs a child flow; a child error end is caught by "
            "the parent's error boundary."
        )


def node_task(process, node):
    return process.task_set.get(flow_task=node)


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def _place_order(self, out_of_stock):
        self.client.post(
            OrderFulfillment.start.reverse("execute"),
            {"out_of_stock": "1" if out_of_stock else "0"},
        )
        # advance the child's async reservation timer to resolve the subprocess
        Task.objects.filter(flow_task_type="TIMER", status=STATUS.SCHEDULED).update(
            scheduled=timezone.now() - timedelta(seconds=1)
        )
        fire_due_timers()
        return FulfillmentProcess.objects.filter(flow_class=OrderFulfillment).latest(
            "pk"
        )

    def test_happy_path_ships(self):
        process = self._place_order(out_of_stock=False)
        process.refresh_from_db()
        self.assertEqual(process.status, STATUS.DONE)
        self.assertTrue(process.data.get("shipped"))
        self.assertEqual(
            node_task(process, OrderFulfillment.fulfill).status, STATUS.DONE
        )

    def test_child_error_end_triggers_parent_backorder(self):
        process = self._place_order(out_of_stock=True)
        process.refresh_from_db()

        self.assertEqual(
            node_task(process, OrderFulfillment.fulfill).status, STATUS.CANCELED
        )
        self.assertEqual(
            node_task(process, OrderFulfillment.fulfill__error).status, STATUS.DONE
        )
        self.assertTrue(process.data.get("backordered"))
        self.assertEqual(process.status, STATUS.DONE)

        child = FulfillmentChildProcess.objects.filter(
            flow_class=FulfillmentChild
        ).latest("pk")
        self.assertEqual(child.data.get("_error", {}).get("code"), "out-of-stock")
