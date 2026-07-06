"""
Pattern:
    An error end event ends the process with a named error: it cancels the
    other active branches, records the error code, and marks the instance
    finished. Inside a subprocess it also signals the parent (see the
    Subprocess pattern).

Example:
    While charging the card and reserving stock in parallel, the payment is
    declined. The charge branch reaches an error end ("payment-failed"),
    which stops the reservation branch and records the failure.

Purpose:
    ``flow.ErrorEnd("code")`` is the BPMN error end event. Unlike a plain end
    it carries a business error and aborts sibling work; the code is stored on
    the process (``data["_error"]["code"]``) for reporting and for a parent
    ``.OnError(code=...)`` boundary to match against.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView
from viewflow.workflow.models import Process
from viewflow.workflow.status import STATUS


class CheckoutProcess(Process):
    class Meta:
        proxy = True


class PaymentError(flow.Flow):
    process_class = CheckoutProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Start Checkout")
        .Permission(auto_create=True)
        .Next(this.split)
    )

    split = flow.Split().Always(this.charge_card).Always(this.reserve_stock)

    charge_card = (
        flow.Function(this.do_charge)
        .Annotation(title="Charge Card")
        .Next(this.payment_failed)
    )

    # parallel branch aborted by the error end
    reserve_stock = flow.Handle().Annotation(title="Reserve Stock").Next(this.reserved)
    reserved = flow.End()

    payment_failed = flow.ErrorEnd("payment-failed").Annotation(title="Payment Failed")

    def do_charge(self, activation):
        # the gateway/service reports a decline
        activation.process.data["charged"] = False
        activation.process.save()

    process_description = (
        "A declined payment reaches an error end that records "
        "'payment-failed' and aborts the parallel stock-reservation branch."
    )

    def __str__(self) -> str:
        return "An error end event finishes the process with a named business error."


def node_task(process, node):
    return process.task_set.get(flow_task=node)


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def test_error_end_records_code_and_aborts_sibling(self):
        self.client.post(PaymentError.start.reverse("execute"), {})
        process = CheckoutProcess.objects.get()

        self.assertEqual(
            node_task(process, PaymentError.reserve_stock).status, STATUS.CANCELED
        )
        self.assertEqual(
            node_task(process, PaymentError.payment_failed).status, STATUS.DONE
        )
        process.refresh_from_db()
        self.assertEqual(process.status, STATUS.DONE)
        self.assertEqual(process.data.get("_error", {}).get("code"), "payment-failed")
