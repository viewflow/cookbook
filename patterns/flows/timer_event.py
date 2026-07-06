"""
Pattern:
    An intermediate timer event pauses the process for a fixed delay (or
    until an absolute moment), then continues on its own.

Example:
    After an invoice is issued, wait 30 seconds and then send a payment
    reminder.

Purpose:
    ``flow.Timer`` is a database-backed wait. The process sits in the
    ``SCHEDULED`` state; a periodic dispatcher (the ``workflow_timers``
    management command, or the celery-beat ``workflow_fire_timers`` task)
    fires due timers and resumes the flow. Nothing is blocked or polled in a
    request -- the wait survives restarts.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView
from viewflow.workflow.models import Process, Task
from viewflow.workflow.status import STATUS
from viewflow.workflow.timers import fire_due_timers


class ReminderProcess(Process):
    class Meta:
        proxy = True


class TimerDelay(flow.Flow):
    process_class = ReminderProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=[]))
        .Annotation(title="Issue Invoice")
        .Permission(auto_create=True)
        .Next(this.wait)
    )

    wait = (
        flow.Timer(timedelta(seconds=30))
        .Annotation(title="Wait 30s")
        .Next(this.send_reminder)
    )

    send_reminder = (
        flow.SendHandle(this.do_send_reminder)
        .Annotation(title="Send Reminder")
        .Next(this.end)
    )

    end = flow.End()

    def do_send_reminder(self, activation):
        activation.process.data["reminded"] = True
        activation.process.save()

    process_description = (
        "After the invoice is issued the process waits, then the timer fires "
        "and a payment reminder is sent."
    )

    def __str__(self) -> str:
        return "An intermediate timer event delays the process, then it continues on its own."


class Test(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        User.objects.create_superuser(username="admin", password="admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def test_timer_waits_then_fires(self):
        self.client.post(TimerDelay.start.reverse("execute"), {})
        process = ReminderProcess.objects.get()

        timer_task = process.task_set.get(flow_task=TimerDelay.wait)
        self.assertEqual(timer_task.status, STATUS.SCHEDULED)

        # nothing is due yet
        self.assertEqual(fire_due_timers(), 0)

        # make it due and run the dispatcher
        Task.objects.filter(pk=timer_task.pk).update(
            scheduled=timezone.now() - timedelta(seconds=1)
        )
        self.assertEqual(fire_due_timers(), 1)

        process.refresh_from_db()
        self.assertEqual(process.status, STATUS.DONE)
        self.assertTrue(process.data["reminded"])
