"""
Pattern:
    A boundary timer is attached to a task. If the task is not finished
    before the timer elapses, the boundary fires. An *interrupting* boundary
    cancels the task and diverts the flow; a *non-interrupting* one leaves
    the task running and starts a parallel path.

Example:
    An approval must be handled within a deadline. A non-interrupting timer
    sends a reminder along the way; the interrupting timer escalates and
    withdraws the approval if the deadline passes.

Purpose:
    ``.OnTimeout(delay, then, interrupting=True/False)`` on the host task is
    the BPMN boundary timer event. It is armed alongside the host task,
    scheduled like a ``flow.Timer``, and fired by the same dispatcher. When
    the host finishes first, every boundary on it is cancelled.
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process, Task
from viewflow.workflow.status import STATUS
from viewflow.workflow.timers import fire_due_timers


class ApprovalDeadlineProcess(Process):
    class Meta:
        proxy = True


class ApprovalTimeout(flow.Flow):
    process_class = ApprovalDeadlineProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Submit for Approval")
        .Permission(auto_create=True)
        .Next(this.approve)
    )

    approve = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Annotation(title="Approve Request")
        # interrupting escalation past the deadline -> approve__timeout
        .OnTimeout(timedelta(seconds=45), this.escalated, title="Escalate")
        # non-interrupting reminder along the way -> approve__timeout_2
        .OnTimeout(
            timedelta(seconds=20), this.reminded, interrupting=False, title="Reminder"
        )
        .Next(this.end)
    )

    reminded = flow.End()
    escalated = flow.End()
    end = flow.End()

    process_description = (
        "A reminder is sent partway to the deadline (non-interrupting); if the "
        "deadline passes the approval is escalated and withdrawn (interrupting)."
    )

    def __str__(self) -> str:
        return (
            "Boundary timers on a task send a reminder and, past the deadline, "
            "escalate by cancelling the task."
        )


def node_task(process, node):
    return process.task_set.get(flow_task=node)


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def _start(self):
        self.client.post(ApprovalTimeout.start.reverse("execute"), {})
        return ApprovalDeadlineProcess.objects.latest("pk")

    def test_approval_in_time_cancels_boundaries(self):
        process = self._start()
        approve = node_task(process, ApprovalTimeout.approve)
        self.client.post(approve.reverse("assign"), {})
        self.client.post(approve.reverse("execute"), {})

        self.assertEqual(
            node_task(process, ApprovalTimeout.approve__timeout).status,
            STATUS.CANCELED,
        )
        self.assertEqual(
            node_task(process, ApprovalTimeout.approve__timeout_2).status,
            STATUS.CANCELED,
        )
        process.refresh_from_db()
        self.assertEqual(process.status, STATUS.DONE)

    def test_non_interrupting_reminder_keeps_task_active(self):
        process = self._start()
        Task.objects.filter(
            pk=node_task(process, ApprovalTimeout.approve__timeout_2).pk
        ).update(scheduled=timezone.now() - timedelta(seconds=1))
        self.assertEqual(fire_due_timers(), 1)

        # reminder path completed, approval still waiting
        self.assertEqual(
            node_task(process, ApprovalTimeout.reminded).status, STATUS.DONE
        )
        self.assertEqual(node_task(process, ApprovalTimeout.approve).status, STATUS.NEW)
        process.refresh_from_db()
        self.assertEqual(process.status, STATUS.NEW)

    def test_deadline_escalates_and_withdraws(self):
        process = self._start()
        # by the deadline both boundary timers are due
        Task.objects.filter(
            process=process, flow_task_type="TIMER", status=STATUS.SCHEDULED
        ).update(scheduled=timezone.now() - timedelta(seconds=1))
        fire_due_timers()

        # the interrupting escalation withdraws the approval
        self.assertEqual(
            node_task(process, ApprovalTimeout.approve).status, STATUS.CANCELED
        )
        self.assertEqual(
            node_task(process, ApprovalTimeout.escalated).status, STATUS.DONE
        )
        process.refresh_from_db()
        self.assertEqual(process.status, STATUS.DONE)
