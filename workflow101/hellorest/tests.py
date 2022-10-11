from django.urls import path
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from viewflow.workflow.flow import FlowViewset
from viewflow.workflow.models import Process, Task

from .flows import HelloRestFlow


@override_settings(
    ROOT_URLCONF=__name__,
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
)
class Test(TestCase):  # noqa: D101
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "password")
        self.assertTrue(self.client.login(username="admin", password="password"))

    def reverse(self, flow_task, name):
        task = Task.objects.get(flow_task=flow_task)
        return flow_task.reverse(name, args=[task.process_id, task.pk])

    def _testApproved(self):
        self.assertRedirects(
            self.client.post(
                "/workflow/start/",
                {"text": "Hello, world", "_viewflow_activation-started": "2000-01-01", "_continue": 1},
            ),
            self.reverse(HelloRestFlow.approve, "index"),
            fetch_redirect_response=False,
        )

        self.assertRedirects(
            self.client.post(self.reverse(HelloRestFlow.approve, "assign"), {"_continue": 1}),
            self.reverse(HelloRestFlow.approve, "index"),
            fetch_redirect_response=False
        )

        self.assertEqual(
            self.client.post(
                self.reverse(HelloRestFlow.approve, "execute"),
                {"approved": True, "_viewflow_activation-started": "2000-01-01"},
            ).status_code,
            302,
        )

        process = Process.objects.get()

        self.assertEquals("DONE", process.status)
        self.assertEquals(5, process.task_set.count())

    def _testNotApproved(self):
        self.assertRedirects(
            self.client.post(
                "/workflow/start/",
                {"text": "Hello, world", "_viewflow_activation-started": "2000-01-01", "_continue": 1},
            ),
            self.reverse(HelloRestFlow.approve, "index"),
            fetch_redirect_response=False
        )

        self.assertRedirects(
            self.client.post(self.reverse(HelloRestFlow.approve, "assign"), {"_continue": 1}),
            self.reverse(HelloRestFlow.approve, "index"),
            fetch_redirect_response=False
        )

        self.assertEqual(
            self.client.post(
                self.reverse(HelloRestFlow.approve, "execute"),
                {"approved": False, "_viewflow_activation-started": "2000-01-01"},
            ).status_code,
            302
        )

        process = Process.objects.get()

        self.assertEquals("DONE", process.status)
        self.assertEquals(4, process.task_set.count())


urlpatterns = [path("api/", FlowViewset(HelloRestFlow).urls)]
