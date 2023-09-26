from django.urls import path
from django.contrib.auth.models import User, Permission
from django.test import TestCase, override_settings
from viewflow.workflow.flow import FlowViewset
from viewflow.workflow.models import Process, Task

from .flows import HelloWorldFlow


@override_settings(
    ROOT_URLCONF=__name__,
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
)
class Test(TestCase):  # noqa: D101
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(username="admin", password="admin")

        cls.employee = User.objects.create_user(
            username="employee", password="employee"
        )
        cls.employee.user_permissions.add(
            Permission.objects.get(codename="view_helloworldprocess")
        )
        cls.employee.user_permissions.add(
            Permission.objects.get(codename="can_start_helloworldprocess")
        )

        cls.manager = User.objects.create_user(username="manager", password="manager")
        cls.manager.user_permissions.add(
            Permission.objects.get(codename="view_helloworldprocess")
        )
        cls.manager.user_permissions.add(
            Permission.objects.get(codename="can_approve_helloworldprocess")
        )

    def reverse(self, flow_task, name):
        task = Task.objects.get(flow_task=flow_task)
        return flow_task.reverse(name, args=[task.process_id, task.pk])

    def test_approved_flow(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        self.assertRedirects(
            self.client.post(
                "/workflow/start/",
                {
                    "text": "Hello, world",
                    "_viewflow_activation-started": "2000-01-01",
                    "_continue": 1,
                },
            ),
            self.reverse(HelloWorldFlow.approve, "index"),
            fetch_redirect_response=False,
        )

        self.assertRedirects(
            self.client.post(
                self.reverse(HelloWorldFlow.approve, "assign"), {"_continue": 1}
            ),
            self.reverse(HelloWorldFlow.approve, "index"),
            fetch_redirect_response=False,
        )

        self.assertEqual(
            self.client.post(
                self.reverse(HelloWorldFlow.approve, "execute"),
                {"approved": True, "_viewflow_activation-started": "2000-01-01"},
            ).status_code,
            302,
        )

        process = Process.objects.get()

        self.assertEquals("DONE", process.status)
        self.assertEquals(5, process.task_set.count())

    def test_not_approved_flow(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))
        self.assertRedirects(
            self.client.post(
                "/workflow/start/",
                {
                    "text": "Hello, world",
                    "_viewflow_activation-started": "2000-01-01",
                    "_continue": 1,
                },
            ),
            self.reverse(HelloWorldFlow.approve, "index"),
            fetch_redirect_response=False,
        )

        self.assertRedirects(
            self.client.post(
                self.reverse(HelloWorldFlow.approve, "assign"), {"_continue": 1}
            ),
            self.reverse(HelloWorldFlow.approve, "index"),
            fetch_redirect_response=False,
        )

        self.assertEqual(
            self.client.post(
                self.reverse(HelloWorldFlow.approve, "execute"),
                {"approved": False, "_viewflow_activation-started": "2000-01-01"},
            ).status_code,
            302,
        )

        process = Process.objects.get()

        self.assertEquals("DONE", process.status)
        self.assertEquals(4, process.task_set.count())

    def test_users_collaboration_flow(self):
        self.assertTrue(self.client.login(username="employee", password="employee"))

        # Start process
        response = self.client.post(
            "/workflow/start/",
            {
                "text": "Hello, world",
                "_viewflow_activation-started": "2000-01-01",
                "_continue": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        process = Process.objects.get()
        self.assertEquals("NEW", process.status)
        self.assertEquals(2, process.task_set.count())

        # login as manager and assign the task
        self.assertTrue(self.client.login(username="manager", password="manager"))
        response = self.client.post(
            self.reverse(HelloWorldFlow.approve, "assign"), {"_continue": 1}
        )
        self.assertEqual(response.status_code, 302)

        # Approve it
        response = self.client.post(
            self.reverse(HelloWorldFlow.approve, "execute"),
            {"approved": True, "_viewflow_activation-started": "2000-01-01"},
        )
        self.assertEqual(response.status_code, 302)

        process = Process.objects.get()
        self.assertEquals("DONE", process.status)
        self.assertEquals(5, process.task_set.count())

    def test_access_protection(self):
        # Try to start a process as the manager
        self.assertTrue(self.client.login(username="manager", password="manager"))
        response = self.client.post(
            "/workflow/start/",
            {
                "text": "Hello, world",
                "_viewflow_activation-started": "2000-01-01",
                "_continue": 1,
            },
        )
        self.assertEqual(response.status_code, 403)

        # Start process as  employee
        self.assertTrue(self.client.login(username="employee", password="employee"))
        response = self.client.post(
            "/workflow/start/",
            {
                "text": "Hello, world",
                "_viewflow_activation-started": "2000-01-01",
                "_continue": 1,
            },
        )
        self.assertEqual(response.status_code, 302)

        # Try to assign approve task to the employee
        response = self.client.post(
            self.reverse(HelloWorldFlow.approve, "assign"), {"_continue": 1}
        )
        self.assertEqual(response.status_code, 403)


urlpatterns = [path("workflow/", FlowViewset(HelloWorldFlow).urls)]
