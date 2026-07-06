"""
Pattern:
    A saga undoes already-completed steps when a later step fails. Each step
    registers a compensation handler; a compensation throw event then runs
    those handlers for the completed steps in reverse order.

Example:
    Book a flight, then a hotel, then take payment. If payment fails, the
    process compensates: cancel the hotel, then cancel the flight.

Purpose:
    ``node.CompensateWith(this.handler)`` attaches an undo action to a step,
    and ``flow.CompensateThrow()`` triggers every registered handler for the
    completed steps, newest first. This is BPMN's compensation -- the standard
    way to keep long-running, non-transactional work consistent.
"""

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.workflow import act, flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process
from viewflow.workflow.status import STATUS


# records the order compensation handlers fire in (see the test)
COMPENSATED = []


class BookingProcess(Process):
    paid = jsonstore.BooleanField(
        default=False, choices=((1, "Payment confirmed"), (0, "Payment failed"))
    )

    class Meta:
        proxy = True


class PayForm(forms.ModelForm):
    class Meta:
        model = BookingProcess
        fields = ["paid"]
        widgets = {"paid": forms.RadioSelect()}


class BookingSaga(flow.Flow):
    process_class = BookingProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Start Booking")
        .Permission(auto_create=True)
        .Next(this.book_flight)
    )

    book_flight = (
        flow.Function(this.do_book_flight)
        .CompensateWith(this.cancel_flight)
        .Annotation(title="Book Flight")
        .Next(this.book_hotel)
    )
    cancel_flight = flow.Function(this.do_cancel_flight).Annotation(
        title="Cancel Flight"
    )

    book_hotel = (
        flow.Function(this.do_book_hotel)
        .CompensateWith(this.cancel_hotel)
        .Annotation(title="Book Hotel")
        .Next(this.pay)
    )
    cancel_hotel = flow.Function(this.do_cancel_hotel).Annotation(title="Cancel Hotel")

    pay = (
        flow.View(UpdateProcessView.as_view(form_class=PayForm))
        .Annotation(title="Take Payment")
        .Next(this.check)
    )

    check = (
        flow.If(act.process.paid)
        .Annotation(title="Paid?")
        .Then(this.confirmed)
        .Else(this.compensate)
    )

    compensate = flow.CompensateThrow().Annotation(title="Compensate").Next(this.failed)

    confirmed = flow.End()
    failed = flow.End()

    def do_book_flight(self, activation):
        activation.process.data["flight"] = "booked"
        activation.process.save()

    def do_book_hotel(self, activation):
        activation.process.data["hotel"] = "booked"
        activation.process.save()

    def do_cancel_flight(self, activation):
        COMPENSATED.append("flight")

    def do_cancel_hotel(self, activation):
        COMPENSATED.append("hotel")

    process_description = (
        "Book flight, then hotel, then take payment. If payment fails the saga "
        "cancels the hotel and then the flight -- compensation in reverse order."
    )

    def __str__(self) -> str:
        return (
            "A saga compensates completed steps in reverse order when a later "
            "step fails."
        )


def node_task(process, node):
    return process.task_set.get(flow_task=node)


class Test(TestCase):
    def setUp(self):
        del COMPENSATED[:]
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def _run(self, paid):
        self.client.post(BookingSaga.start.reverse("execute"), {})
        process = BookingProcess.objects.latest("pk")
        pay = node_task(process, BookingSaga.pay)
        self.client.post(pay.reverse("assign"), {})
        self.client.post(pay.reverse("execute"), {"paid": "1" if paid else "0"})
        process.refresh_from_db()
        return process

    def test_payment_success_no_compensation(self):
        process = self._run(paid=True)
        self.assertEqual(process.status, STATUS.DONE)
        self.assertEqual(node_task(process, BookingSaga.confirmed).status, STATUS.DONE)
        self.assertEqual(COMPENSATED, [])

    def test_payment_failure_compensates_in_reverse(self):
        process = self._run(paid=False)
        self.assertEqual(process.status, STATUS.DONE)
        self.assertEqual(node_task(process, BookingSaga.failed).status, STATUS.DONE)
        # handlers fire newest-completed first: hotel was booked after flight
        self.assertEqual(COMPENSATED, ["hotel", "flight"])
