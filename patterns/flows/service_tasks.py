"""
Pattern:
    Automatic steps that a system performs without a human: a send task
    dispatches an outbound message, a business rule task evaluates a
    decision rule. Both run synchronously as the process passes through.

Example:
    When an order is placed, the process sends the confirmation e-mail
    (send task) and then computes the loyalty discount (business rule task).

Purpose:
    BPMN distinguishes task types so a diagram tells you *how* each step is
    performed. ``flow.SendHandle`` marks an outbound message hook
    (``sendTask``); ``flow.BusinessRule`` marks a rule evaluation
    (``businessRuleTask``). Both behave like ``flow.Function`` -- executed
    synchronously on activation -- but export with the correct BPMN element
    and marker, so the whole flow runs to completion the moment it starts.
"""

from django.test import TestCase
from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView
from viewflow.workflow.models import Process
from viewflow.workflow.status import STATUS


class OnlineOrderProcess(Process):
    class Meta:
        proxy = True


class ServiceTasks(flow.Flow):
    process_class = OnlineOrderProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Place Order")
        .Permission(auto_create=True)
        .Next(this.send_confirmation)
    )

    send_confirmation = (
        flow.SendHandle(this.do_send_confirmation)
        .Annotation(title="Send Confirmation")
        .Next(this.apply_discount)
    )

    apply_discount = (
        flow.BusinessRule(this.do_apply_discount)
        .Annotation(title="Apply Loyalty Discount")
        .Next(this.end)
    )

    end = flow.End()

    def do_send_confirmation(self, activation):
        activation.process.data["confirmation_sent"] = True
        activation.process.save()

    def do_apply_discount(self, activation):
        # a trivial "rule": returning customers get 10% off
        activation.process.data["discount"] = 10
        activation.process.save()

    process_description = (
        "Placing an order sends the confirmation message and then evaluates "
        "the loyalty-discount rule -- both automatic, no human step."
    )

    def __str__(self) -> str:
        return (
            "A send task dispatches a message and a business rule task "
            "evaluates a decision, both performed automatically by the system."
        )


class Test(TestCase):
    def test_send_and_rule_run_automatically(self):
        from django.contrib.auth.models import User

        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

        self.client.post(ServiceTasks.start.reverse("execute"), {})

        process = OnlineOrderProcess.objects.get()
        self.assertEqual(process.status, STATUS.DONE)
        self.assertTrue(process.data["confirmation_sent"])
        self.assertEqual(process.data["discount"], 10)

        send = process.task_set.get(flow_task=ServiceTasks.send_confirmation)
        rule = process.task_set.get(flow_task=ServiceTasks.apply_discount)
        self.assertEqual(send.status, STATUS.DONE)
        self.assertEqual(rule.status, STATUS.DONE)
