"""
Pattern:
    An error boundary is attached to a task. If that task fails, the boundary
    catches the failure, cancels the task, and routes the process to a
    recovery path instead of letting the error bubble up.

Example:
    A deployment step runs in the background. If it throws, the boundary
    catches it and runs a rollback.

Purpose:
    ``.OnError(...)`` attaches a BPMN error boundary event to a task. It
    fires when the host task is marked ``ERROR`` -- a failure recorded in a
    background context (a job or a timer continuation). Here a short
    ``flow.Timer`` hands the deployment off to the dispatcher, so a raised
    exception is recorded on the task and caught by the boundary rather than
    surfacing to the caller.
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


class DeploymentProcess(Process):
    class Meta:
        proxy = True


class DeployRecovery(flow.Flow):
    process_class = DeploymentProcess

    # test-only switch to exercise both the failure and the success path
    should_fail = True

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Trigger Deploy")
        .Permission(auto_create=True)
        .Next(this.handoff)
    )

    handoff = (
        flow.Timer(timedelta(seconds=5))
        .Annotation(title="Queue Deploy")
        .Next(this.deploy)
    )

    deploy = (
        flow.Function(this.run_deploy)
        .Annotation(title="Deploy")
        .OnError(this.rollback, title="On Failure")
        .Next(this.notify_ok)
    )

    notify_ok = (
        flow.SendHandle(this.do_notify_ok)
        .Annotation(title="Notify Success")
        .Next(this.end)
    )

    rollback = (
        flow.Function(this.do_rollback)
        .Annotation(title="Rollback")
        .Next(this.recovered)
    )

    recovered = flow.End()
    end = flow.End()

    def run_deploy(self, activation):
        if type(self).should_fail:
            raise ValueError("deployment failed")
        activation.process.data["deployed"] = True
        activation.process.save()

    def do_notify_ok(self, activation):
        activation.process.data["notified"] = True
        activation.process.save()

    def do_rollback(self, activation):
        activation.process.data["rolled_back"] = True
        activation.process.save()

    process_description = (
        "The deploy step runs in the background; on failure the error boundary "
        "cancels it and runs a rollback."
    )

    def __str__(self) -> str:
        return "An error boundary catches a failing task and routes the process to recovery."


def node_task(process, node):
    return process.task_set.get(flow_task=node)


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def _start_and_fire(self):
        self.client.post(DeployRecovery.start.reverse("execute"), {})
        process = DeploymentProcess.objects.latest("pk")
        Task.objects.filter(pk=node_task(process, DeployRecovery.handoff).pk).update(
            scheduled=timezone.now() - timedelta(seconds=1)
        )
        fire_due_timers()
        process.refresh_from_db()
        return process

    def test_failure_is_caught_and_rolled_back(self):
        DeployRecovery.should_fail = True
        process = self._start_and_fire()

        self.assertEqual(
            node_task(process, DeployRecovery.deploy).status, STATUS.CANCELED
        )
        self.assertEqual(
            node_task(process, DeployRecovery.deploy__error).status, STATUS.DONE
        )
        self.assertEqual(
            node_task(process, DeployRecovery.rollback).status, STATUS.DONE
        )
        self.assertTrue(process.data.get("rolled_back"))
        self.assertEqual(process.status, STATUS.DONE)

    def test_success_path_cancels_the_boundary(self):
        DeployRecovery.should_fail = False
        try:
            process = self._start_and_fire()
        finally:
            DeployRecovery.should_fail = True

        self.assertEqual(node_task(process, DeployRecovery.deploy).status, STATUS.DONE)
        self.assertEqual(
            node_task(process, DeployRecovery.deploy__error).status, STATUS.CANCELED
        )
        self.assertTrue(process.data.get("deployed"))
        self.assertEqual(process.status, STATUS.DONE)
