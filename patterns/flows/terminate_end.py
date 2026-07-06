"""
Pattern:
    A terminate end event ends the whole process at once: every other active
    task in the process is cancelled and the instance finishes immediately.
    A plain end event only ends its own branch.

Example:
    An order is being processed on two parallel branches -- charge the card
    and reserve stock. The customer cancels: one branch reaches a terminate
    end, which stops the still-running reservation branch too.

Purpose:
    ``flow.TerminateEnd`` is the BPMN terminate end event. Use it when
    reaching one outcome must abort all remaining work in the process rather
    than waiting for the other branches to finish.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView
from viewflow.workflow.models import Process
from viewflow.workflow.status import STATUS


class OrderCancelProcess(Process):
    class Meta:
        proxy = True


class RaceTerminate(flow.Flow):
    process_class = OrderCancelProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Start Order")
        .Permission(auto_create=True)
        .Next(this.split)
    )

    split = flow.Split().Always(this.cancel_order).Always(this.reserve_stock)

    cancel_order = (
        flow.Function(this.do_cancel)
        .Annotation(title="Cancel Order")
        .Next(this.terminate)
    )

    # a still-running parallel branch, aborted by the terminate end
    reserve_stock = flow.Handle().Annotation(title="Reserve Stock").Next(this.reserved)
    reserved = flow.End()

    terminate = flow.TerminateEnd().Annotation(title="Terminate")

    def do_cancel(self, activation):
        activation.process.data["cancelled"] = True
        activation.process.save()

    process_description = (
        "One branch cancels the order and hits a terminate end, which aborts "
        "the parallel stock-reservation branch and finishes the process."
    )

    def __str__(self) -> str:
        return "A terminate end event cancels all other active tasks and ends the process at once."


def node_task(process, node):
    return process.task_set.get(flow_task=node)


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def test_terminate_aborts_sibling_branch(self):
        self.client.post(RaceTerminate.start.reverse("execute"), {})
        process = OrderCancelProcess.objects.get()

        self.assertEqual(
            node_task(process, RaceTerminate.reserve_stock).status, STATUS.CANCELED
        )
        self.assertEqual(
            node_task(process, RaceTerminate.terminate).status, STATUS.DONE
        )
        process.refresh_from_db()
        self.assertEqual(process.status, STATUS.DONE)
