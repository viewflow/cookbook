"""
Description
    This rule makes sure that two tasks in a process are handled by
    different people.

Example
    If one person prepares a cheque, another person must sign it.

Motivation
    This rule helps with security and ensures checks and balances. It
    prevents the same person from doing both tasks, making the process more
    trustworthy. In cases where multiple people are working on the same type
    of task, this rule can also make sure that the work is shared fairly,
    with each person handling a different part.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.workflow import flow, STATUS
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process


class SeparationOfDutiesView(flow.View):
    def can_assign(self, user, task):
        """Override to ensure task is not assigned to the same user who completed the previous task."""
        previous_task = task.process.task_set.filter(status=STATUS.DONE).last()
        if previous_task and previous_task.owner == user:
            return False

        return super().can_assign(user, task)


class SeparationOfDutiesProcess(Process):
    cheque_details = jsonstore.CharField(max_length=500)
    countersigned = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True

    def __str__(self):
        return f"SeparationOfDutiesProcess: {self.cheque_details[:50]}"


class SeparationOfDutiesFlow(flow.Flow):
    process_class = SeparationOfDutiesProcess

    prepare_cheque = (
        flow.Start(CreateProcessView.as_view(fields=["cheque_details"]))
        .Annotation(title="Prepare Cheque")
        .Next(this.countersign_cheque)
    )

    countersign_cheque = (
        SeparationOfDutiesView(UpdateProcessView.as_view(fields=["countersigned"]))
        .Annotation(title="Countersign Cheque")
        .Next(this.end)
    )

    end = flow.End()

    process_description = (
        "This process ensures that two tasks, 'Prepare Cheque' and 'Countersign Cheque', "
        "are handled by different users for security and audit purposes."
    )

    def __str__(self):
        return "Separation of Duties Flow"


class TestSeparationOfDutiesFlow(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.user1 = User.objects.create_user(username="user1", password="password")
        cls.user2 = User.objects.create_user(username="user2", password="password")

    def test_flow(self):
        self.client.login(username="user1", password="password")

        # Start the process and prepare the cheque
        response = self.client.post(
            SeparationOfDutiesFlow.prepare_cheque.reverse("execute"),
            {"cheque_details": "Pay to the order of John Doe"},
        )
        self.assertEqual(response.status_code, 302)

        # Verify the cheque preparation task
        process = SeparationOfDutiesProcess.objects.get()
        self.assertEqual(process.cheque_details, "Pay to the order of John Doe")

        # Countersign the cheque with a different user
        self.client.login(username="user2", password="password")
        countersign_task = process.task_set.get(
            flow_task=SeparationOfDutiesFlow.countersign_cheque
        )
        self.client.post(countersign_task.reverse("assign"), {})
        response = self.client.post(
            countersign_task.reverse("execute"), {"countersigned": True}
        )
        self.assertEqual(response.status_code, 302)

        # Verify process completion
        process.refresh_from_db()
        self.assertTrue(process.countersigned)
