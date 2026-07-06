"""
Pattern:
    A timer start event kicks off a fresh process instance on a schedule --
    no user, no upstream task. The first instance starts on the first
    dispatcher sweep, then again every interval.

Example:
    Every 10 minutes, start a process that compiles and files a status
    report.

Purpose:
    ``flow.StartTimer(interval=...)`` is the BPMN timer start event. The same
    dispatcher that fires ``flow.Timer`` (``workflow_timers`` /
    ``workflow_fire_timers``) creates a new process whenever the interval has
    elapsed since the last run -- a recurring, durable cron built into the
    flow.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.models import Process, Task
from viewflow.workflow.status import STATUS
from viewflow.workflow.timers import fire_due_start_timers


class ScheduledReportProcess(Process):
    class Meta:
        proxy = True


class ScheduledReport(flow.Flow):
    process_class = ScheduledReportProcess

    start = (
        flow.StartTimer(interval=timedelta(minutes=10))
        .Annotation(title="Every 10 min")
        .Next(this.build_report)
    )

    build_report = (
        flow.BusinessRule(this.do_build_report)
        .Annotation(title="Compile Report")
        .Next(this.end)
    )

    end = flow.End()

    def do_build_report(self, activation):
        activation.process.data["report"] = "compiled"
        activation.process.save()

    process_description = (
        "A timer start event begins a new report process every 10 minutes "
        "without any user action."
    )

    def __str__(self) -> str:
        return (
            "A timer start event starts a new process instance on a recurring schedule."
        )


class Test(TestCase):
    def _processes(self):
        return Process.objects.filter(flow_class=ScheduledReport)

    def test_first_sweep_starts_a_process(self):
        self.assertEqual(fire_due_start_timers(flows=[ScheduledReport]), 1)

        process = self._processes().get()
        self.assertEqual(process.status, STATUS.DONE)
        self.assertEqual(process.data["report"], "compiled")

    def test_not_due_again_until_interval_elapsed(self):
        fire_due_start_timers(flows=[ScheduledReport])
        self.assertEqual(fire_due_start_timers(flows=[ScheduledReport]), 0)
        self.assertEqual(self._processes().count(), 1)

    def test_due_again_after_interval(self):
        fire_due_start_timers(flows=[ScheduledReport])
        Task.objects.filter(
            process__flow_class=ScheduledReport, flow_task_type="START"
        ).update(created=timezone.now() - timedelta(minutes=20))

        self.assertEqual(fire_due_start_timers(flows=[ScheduledReport]), 1)
        self.assertEqual(self._processes().count(), 2)
