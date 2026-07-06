from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import path
from django.utils import timezone

from viewflow.urls import Site
from viewflow.workflow.models import Task
from viewflow.workflow.status import STATUS

from .flows import SnoozeFlow
from .viewsets import SnoozeFlowViewset
from .views import to_iso


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):  # noqa: D101
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create_superuser(username="alice", password="alice")
        cls.bob = User.objects.create_user(username="bob", password="bob")

    def task(self):
        return Task.objects.get(flow_task=SnoozeFlow.review)

    def node_url(self, name):
        task = self.task()
        return SnoozeFlow.review.reverse(name, args=[task.process_id, task.pk])

    def start_process_as(self, username):
        self.assertTrue(self.client.login(username=username, password=username))
        response = self.client.post(
            "/snooze/start/",
            {"_viewflow_activation-started": "2000-01-01", "_continue": 1},
        )
        self.assertEqual(response.status_code, 302)

    def test_task_starts_assigned_to_the_creator(self):
        self.start_process_as("alice")
        task = self.task()
        self.assertEqual(STATUS.ASSIGNED, task.status)
        self.assertEqual(self.alice, task.owner)
        self.assertNotIn("snoozed", task.data)

    def test_snooze_sets_wakeup_and_hides_task_from_inbox(self):
        self.start_process_as("alice")

        response = self.client.post(self.node_url("snooze"), {"until": "1w"})
        self.assertEqual(response.status_code, 302)

        task = self.task()
        # still owned by alice, status unchanged -- snooze is pure UI state
        self.assertEqual(STATUS.ASSIGNED, task.status)
        self.assertEqual(self.alice, task.owner)
        self.assertGreater(task.data["snoozed"], to_iso(timezone.now()))

        # gone from the inbox, present in the snoozed list
        inbox = self.client.get("/snooze/inbox/")
        self.assertNotIn(task, inbox.context["object_list"])
        snoozed = self.client.get("/snooze/snoozed/")
        self.assertIn(task, snoozed.context["object_list"])

    def test_unsnooze_returns_the_task_to_the_inbox(self):
        self.start_process_as("alice")
        self.client.post(self.node_url("snooze"), {"until": "1w"})

        response = self.client.post(self.node_url("unsnooze"))
        self.assertEqual(response.status_code, 302)

        task = self.task()
        self.assertNotIn("snoozed", task.data)
        inbox = self.client.get("/snooze/inbox/")
        self.assertIn(task, inbox.context["object_list"])
        snoozed = self.client.get("/snooze/snoozed/")
        self.assertNotIn(task, snoozed.context["object_list"])

    def test_a_snooze_in_the_past_reappears_in_the_inbox(self):
        # No background worker: a task is snoozed only while its wake-up time is
        # in the future. Once it passes, the same query surfaces it again.
        self.start_process_as("alice")
        task = self.task()
        task.data["snoozed"] = to_iso(timezone.now() - timedelta(hours=1))
        task.save(update_fields=["data"])

        inbox = self.client.get("/snooze/inbox/")
        self.assertIn(task, inbox.context["object_list"])
        snoozed = self.client.get("/snooze/snoozed/")
        self.assertNotIn(task, snoozed.context["object_list"])

    def test_a_stranger_cannot_snooze_the_task(self):
        self.start_process_as("alice")  # owned by alice
        snooze_url = self.node_url("snooze")

        # bob is neither the owner nor a flow manager
        self.assertTrue(self.client.login(username="bob", password="bob"))
        response = self.client.post(snooze_url, {"until": "1w"})
        self.assertEqual(response.status_code, 403)
        self.assertNotIn("snoozed", self.task().data)

    def test_snoozed_menu_entry_is_rendered(self):
        self.start_process_as("alice")
        response = self.client.get("/snooze/inbox/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/snooze/snoozed/")
        self.assertContains(response, "Snoozed")


site = Site(viewsets=[SnoozeFlowViewset(SnoozeFlow, icon="snooze")])

urlpatterns = [path("", site.urls)]
