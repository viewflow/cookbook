from __future__ import absolute_import

import os
from celery import Celery

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookbook.patterns.config.settings")

app = Celery("workflow101")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Fire due workflow timers (flow.Timer / flow.StartTimer / boundary timers) so
# the Events/Transactions pattern demos advance. Run a celery beat alongside
# the worker (``celery ... worker -B``) or a cron ``manage.py workflow_timers``.
app.conf.beat_schedule = {
    "viewflow-timers": {
        "task": "viewflow.workflow.tasks.workflow_fire_timers",
        "schedule": 15.0,
    },
}
