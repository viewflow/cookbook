"""
Pattern:
    A manual task is work a person does *outside* of any system -- the
    engine only tracks that it happened. It appears in the task list and is
    marked done with a plain confirmation (no data entry). A following human
    decision then routes the process.

Example:
    A warehouse worker physically packs the parcel (manual task), then picks
    the shipping speed, which sends the process down the express or the
    standard dispatch branch.

Purpose:
    ``flow.ManualTask`` is the BPMN ``manualTask`` -- distinct from a
    ``userTask`` because no form/data is captured, only completion. Pairing
    it with a decision ``View`` shows how a person can both perform offline
    work and steer the flow.
"""

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.workflow import act, flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process
from viewflow.workflow.status import STATUS


class ShipmentProcess(Process):
    express = jsonstore.BooleanField(
        default=False, choices=((1, "Express"), (0, "Standard"))
    )

    class Meta:
        proxy = True


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShipmentProcess
        fields = ["express"]
        widgets = {"express": forms.RadioSelect()}


class ManualHandover(flow.Flow):
    process_class = ShipmentProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Create Shipment")
        .Permission(auto_create=True)
        .Next(this.pack_parcel)
    )

    pack_parcel = (
        flow.ManualTask().Annotation(title="Pack Parcel").Next(this.choose_shipping)
    )

    choose_shipping = (
        flow.View(UpdateProcessView.as_view(form_class=ShippingForm))
        .Annotation(title="Choose Shipping")
        .Next(this.route)
    )

    route = (
        flow.If(act.process.express)
        .Annotation(title="Express?")
        .Then(this.express_dispatch)
        .Else(this.standard_dispatch)
    )

    express_dispatch = (
        flow.SendHandle(this.do_express)
        .Annotation(title="Express Dispatch")
        .Next(this.end)
    )

    standard_dispatch = (
        flow.SendHandle(this.do_standard)
        .Annotation(title="Standard Dispatch")
        .Next(this.end)
    )

    end = flow.End()

    def do_express(self, activation):
        activation.process.data["carrier"] = "overnight"
        activation.process.save()

    def do_standard(self, activation):
        activation.process.data["carrier"] = "ground"
        activation.process.save()

    process_description = (
        "The parcel is packed by hand (manual task), then the chosen shipping "
        "speed routes the process to express or standard dispatch."
    )

    def __str__(self) -> str:
        return (
            "A manual task records offline work, and a following human "
            "decision routes the process down one of two branches."
        )


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def _run(self, express):
        self.client.post(ManualHandover.start.reverse("execute"), {})
        process = ShipmentProcess.objects.latest("pk")

        # manual task: assign + confirm, no fields
        pack = process.task_set.get(flow_task=ManualHandover.pack_parcel)
        self.client.post(pack.reverse("assign"), {"_continue": 1})
        self.client.post(pack.reverse("execute"), {"_continue": 1})

        # human decision routes the flow
        choose = process.task_set.get(flow_task=ManualHandover.choose_shipping)
        self.client.post(choose.reverse("assign"), {})
        self.client.post(
            choose.reverse("execute"), {"express": "1" if express else "0"}
        )

        process.refresh_from_db()
        return process

    def test_express_branch(self):
        process = self._run(express=True)
        self.assertEqual(process.status, STATUS.DONE)
        self.assertEqual(process.data["carrier"], "overnight")
        process.task_set.get(flow_task=ManualHandover.express_dispatch)

    def test_standard_branch(self):
        process = self._run(express=False)
        self.assertEqual(process.status, STATUS.DONE)
        self.assertEqual(process.data["carrier"], "ground")
        process.task_set.get(flow_task=ManualHandover.standard_dispatch)
