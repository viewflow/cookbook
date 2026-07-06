from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import path

from viewflow.workflow.flow import FlowViewset
from viewflow.workflow.models import Process
from viewflow.workflow.status import STATUS

from .flows import ItemFlow, OrderFlow
from .viewsets import OrderFlowViewset


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):  # noqa: D101
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create_superuser(username="alice", password="alice")
        cls.bob = User.objects.create_user(username="bob", password="bob")

    def start_order_as(self, username, first_item="Widget"):
        self.assertTrue(self.client.login(username=username, password=username))
        response = self.client.post(
            "/orders/start/",
            {"title": first_item, "_viewflow_activation-started": "2000-01-01"},
        )
        self.assertEqual(response.status_code, 302)
        return Process.objects.get(flow_class=OrderFlow)

    def fulfill_task(self, order):
        return order.task_set.get(flow_task=OrderFlow.fulfill)

    def item_processes(self, order):
        return Process.objects.filter(
            flow_class=ItemFlow, parent_task=self.fulfill_task(order)
        ).order_by("pk")

    def pack(self, item_process):
        task = item_process.task_set.get(flow_task=ItemFlow.pack)
        return self.client.post(
            f"/items/{item_process.pk}/pack/{task.pk}/execute/",
            {"_viewflow_activation-started": "2000-01-01"},
        )

    def test_order_starts_one_item_subprocess(self):
        order = self.start_order_as("alice")
        self.assertEqual(STATUS.STARTED, self.fulfill_task(order).status)
        items = self.item_processes(order)
        self.assertEqual(1, items.count())
        self.assertEqual("Widget", items.first().data["item"]["title"])

    def test_add_item_attaches_another_subprocess_while_running(self):
        order = self.start_order_as("alice")

        response = self.client.post(f"/orders/{order.pk}/add-item/", {"title": "Extra"})
        self.assertEqual(response.status_code, 302)

        items = self.item_processes(order)
        self.assertEqual(2, items.count())
        self.assertEqual(["Widget", "Extra"], [p.data["item"]["title"] for p in items])
        # the parent join is still open, waiting on both children
        self.assertEqual(STATUS.STARTED, self.fulfill_task(order).status)
        self.assertEqual(STATUS.NEW, Process.objects.get(pk=order.pk).status)

    def test_order_completes_only_after_every_item_including_the_added_one(self):
        order = self.start_order_as("alice")
        self.client.post(f"/orders/{order.pk}/add-item/", {"title": "Extra"})

        first, second = list(self.item_processes(order))

        self.assertEqual(302, self.pack(first).status_code)
        # one still pending -> order not done
        self.assertEqual(STATUS.NEW, Process.objects.get(pk=order.pk).status)

        self.assertEqual(302, self.pack(second).status_code)
        # all children done -> NSubprocess joins, order finishes
        self.assertEqual(STATUS.DONE, Process.objects.get(pk=order.pk).status)
        self.assertEqual(STATUS.DONE, self.fulfill_task(order).status)

    def test_cannot_add_item_once_the_order_is_done(self):
        order = self.start_order_as("alice")
        self.pack(self.item_processes(order).first())
        self.assertEqual(STATUS.DONE, Process.objects.get(pk=order.pk).status)

        before = self.item_processes(order).count()
        response = self.client.post(f"/orders/{order.pk}/add-item/", {"title": "Late"})
        self.assertEqual(response.status_code, 302)  # redirected with a message
        self.assertEqual(before, self.item_processes(order).count())

    def test_a_stranger_cannot_add_items(self):
        order = self.start_order_as("alice")

        self.assertTrue(self.client.login(username="bob", password="bob"))
        response = self.client.post(f"/orders/{order.pk}/add-item/", {"title": "Nope"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(1, self.item_processes(order).count())

    def test_add_item_action_shows_on_the_process_detail_page(self):
        order = self.start_order_as("alice")
        response = self.client.get(f"/orders/{order.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"/orders/{order.pk}/add-item/")
        self.assertContains(response, "Add item")


urlpatterns = [
    path("orders/", OrderFlowViewset(OrderFlow).urls),
    path("items/", FlowViewset(ItemFlow).urls),
]
