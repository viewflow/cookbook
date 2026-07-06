from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import path

from viewflow.workflow.flow import FlowViewset
from viewflow.workflow.models import Process, Task
from viewflow.workflow.status import STATUS

from .flows import SubstituteFlow


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):  # noqa: D101
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create_superuser(username="alice", password="alice")
        cls.bob = User.objects.create_user(username="bob", password="bob")

    def reverse(self, flow_task, name):
        task = Task.objects.get(flow_task=flow_task)
        return flow_task.reverse(name, args=[task.process_id, task.pk])

    def start_process_as(self, username):
        self.assertTrue(self.client.login(username=username, password=username))
        response = self.client.post(
            "/workflow/start/",
            {"_viewflow_activation-started": "2000-01-01", "_continue": 1},
        )
        self.assertEqual(response.status_code, 302)

    def test_task_starts_assigned_to_the_creator(self):
        self.start_process_as("alice")
        task = Task.objects.get(flow_task=SubstituteFlow.approve)
        self.assertEqual(STATUS.ASSIGNED, task.status)
        self.assertEqual(self.alice, task.owner)

    def test_substitute_reassigns_the_task_to_another_user(self):
        self.start_process_as("alice")

        response = self.client.post(
            self.reverse(SubstituteFlow.approve, "reassign"),
            {"user": self.bob.pk, "_continue": 1},
        )
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(flow_task=SubstituteFlow.approve)
        # still assigned, but to the substitute now
        self.assertEqual(STATUS.ASSIGNED, task.status)
        self.assertEqual(self.bob, task.owner)

    def test_reassign_action_button_shows_on_the_task_detail(self):
        self.start_process_as("alice")

        response = self.client.get(self.reverse(SubstituteFlow.approve, "detail"))
        self.assertEqual(response.status_code, 200)
        # the button auto-renders because a URL named "reassign" now resolves
        reassign_url = self.reverse(SubstituteFlow.approve, "reassign")
        self.assertContains(response, reassign_url)

    def test_current_owner_is_not_offered_as_a_substitute(self):
        self.start_process_as("alice")

        response = self.client.get(self.reverse(SubstituteFlow.approve, "reassign"))
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertNotIn(self.alice, list(form.fields["user"].queryset))
        self.assertIn(self.bob, list(form.fields["user"].queryset))

    def test_a_stranger_cannot_reassign_the_task(self):
        self.start_process_as("alice")  # owned by alice

        # bob is neither the owner nor a flow manager
        self.assertTrue(self.client.login(username="bob", password="bob"))
        response = self.client.post(
            self.reverse(SubstituteFlow.approve, "reassign"),
            {"user": self.bob.pk, "_continue": 1},
        )
        self.assertEqual(response.status_code, 403)

        task = Task.objects.get(flow_task=SubstituteFlow.approve)
        self.assertEqual(self.alice, task.owner)

    def test_unassign_returns_the_task_to_the_queue(self):
        # The base "cover for me" case needs no custom code: the owner unassigns
        # and any other user can then grab the task from the queue.
        self.start_process_as("alice")

        response = self.client.post(
            self.reverse(SubstituteFlow.approve, "unassign"), {"_continue": 1}
        )
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(flow_task=SubstituteFlow.approve)
        self.assertEqual(STATUS.NEW, task.status)
        self.assertIsNone(task.owner)

        # bob grabs it from the queue
        self.assertTrue(self.client.login(username="bob", password="bob"))
        response = self.client.post(
            self.reverse(SubstituteFlow.approve, "assign"), {"_continue": 1}
        )
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(flow_task=SubstituteFlow.approve)
        self.assertEqual(STATUS.ASSIGNED, task.status)
        self.assertEqual(self.bob, task.owner)


urlpatterns = [path("workflow/", FlowViewset(SubstituteFlow).urls)]
