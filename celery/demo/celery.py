from __future__ import absolute_import, unicode_literals
import os
import celery

from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

app = celery.Celery('demo')

if celery.VERSION < (4, 0):
     app.config_from_object('django.conf:settings')
     app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
else:
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()