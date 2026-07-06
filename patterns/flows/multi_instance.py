"""
Pattern:
    A multi-instance activity runs the same subprocess once per item in a
    collection. Sequential multi-instance runs them one at a time -- the next
    child starts only after the previous one finishes -- and the parent
    continues once every item is done.

Example:
    A purchase needs sign-off from three approvers in order. Each approval is
    an instance of the same review subprocess, run one after another.

Purpose:
    ``flow.NSubprocess(Child.start, items, sequential=True)`` is the BPMN
    sequential multi-instance marker. Pending items are stored on the task and
    the next child is spawned as each one completes -- useful when instances
    must not overlap (ordered approvals, rate-limited calls).
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView
from viewflow.workflow.models import Process, Task
from viewflow.workflow.status import STATUS
from viewflow.workflow.timers import fire_due_timers


class BatchReviewProcess(Process):
    class Meta:
        proxy = True


class ReviewChildProcess(Process):
    class Meta:
        proxy = True


class ReviewChild(flow.Flow):
    process_class = ReviewChildProcess

    start = flow.StartHandle(this.init).Next(this.review)
    # the review runs asynchronously, so each child finishes in its own
    # transaction and the parent can spawn the next one in order
    review = (
        flow.Timer(timedelta(seconds=5)).Annotation(title="Review").Next(this.sign_off)
    )
    sign_off = (
        flow.BusinessRule(this.do_sign_off).Annotation(title="Sign Off").Next(this.end)
    )
    end = flow.End()

    def init(self, activation, item=None):
        activation.process.data["approver"] = item
        activation.process.save()

    def do_sign_off(self, activation):
        activation.process.data["signed"] = True
        activation.process.save()

    def __str__(self) -> str:
        return "A single approver's review, run as one multi-instance child."


class BatchReview(flow.Flow):
    process_class = BatchReviewProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Submit for Review")
        .Permission(auto_create=True)
        .Next(this.approvals)
    )

    approvals = (
        flow.NSubprocess(
            ReviewChild.start,
            lambda process: ["finance", "legal", "director"],
            sequential=True,
        )
        .Annotation(title="Ordered Approvals")
        .Next(this.end)
    )

    end = flow.End()

    process_description = (
        "Three approvers sign off one after another; each is an instance of the "
        "same review subprocess, run sequentially."
    )

    def __str__(self) -> str:
        return "A sequential multi-instance activity runs one child per item, one at a time."


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def _children(self):
        return Process.objects.filter(flow_class=ReviewChild).order_by("created")

    def _advance(self):
        # make the current child's review timer due and fire the dispatcher,
        # finishing that child and spawning the next one
        Task.objects.filter(flow_task_type="TIMER", status=STATUS.SCHEDULED).update(
            scheduled=timezone.now() - timedelta(seconds=1)
        )
        fire_due_timers()

    def test_children_run_one_at_a_time(self):
        self.client.post(BatchReview.start.reverse("execute"), {})
        parent = BatchReviewProcess.objects.get(flow_class=BatchReview)

        # only the first child exists so far
        self.assertEqual(self._children().count(), 1)
        self.assertEqual(self._children().first().data["approver"], "finance")

        # finishing each child spawns the next, in order
        self._advance()
        self.assertEqual(
            [c.data["approver"] for c in self._children()], ["finance", "legal"]
        )
        parent.refresh_from_db()
        self.assertEqual(parent.status, STATUS.NEW)

        self._advance()
        self.assertEqual(
            [c.data["approver"] for c in self._children()],
            ["finance", "legal", "director"],
        )

        # last child finishes -> parent completes
        self._advance()
        parent.refresh_from_db()
        self.assertEqual(parent.status, STATUS.DONE)
