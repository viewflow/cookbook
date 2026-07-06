from django.urls import path
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from viewflow.workflow.flow import FlowViewset
from viewflow.workflow.models import Process, Task
from .flows import OrderItemFlow, CustomerVerificationFlow, OrderFlow


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "password")
        self.client.login(username="admin", password="password")

    def testApproved(self):
        # pks are derived from the DB, not hardcoded: on PostgreSQL sequences
        # are not reset between tests, so the ids drift from the 1-based values
        # SQLite happens to reuse.
        response = self.client.post(
            "/workflow/order/order/start/",
            {
                "customer_name": "John Doe",
                "customer_address": "45, Nowhere St, Oclahoma",
                "formset-order_items-0-title": "GLOCK 17 - 9MM/Gen4",
                "formset-order_items-0-quantity": "2",
                "formset-order_items-1-title": "G43 EXTRA POWER MAG SPRING",
                "formset-order_items-1-quantity": "2",
                "formset-order_items-TOTAL_FORMS": "2",
                "formset-order_items-INITIAL_FORMS": "0",
                "_viewflow_activation-started": "2000-01-01",
            },
        )
        order = Process.objects.get(flow_class=OrderFlow)
        self.assertRedirects(response, f"/workflow/order/order/{order.pk}/")

        # verify the customer (subprocess started by the order)
        verification = Process.objects.get(flow_class=CustomerVerificationFlow)
        verify_task = verification.task_set.get(
            flow_task=CustomerVerificationFlow.verify_customer
        )
        response = self.client.post(
            f"/workflow/order/customerverification/{verification.pk}"
            f"/verify_customer/{verify_task.pk}/execute/",
            {"trusted": True, "_viewflow_activation-started": "2000-01-01"},
        )
        self.assertRedirects(
            response, f"/workflow/order/customerverification/{verification.pk}/"
        )

        # one OrderItem subprocess per ordered item
        order_items = list(
            Process.objects.filter(flow_class=OrderItemFlow).order_by("pk")
        )
        self.assertEqual(2, len(order_items))

        for item in order_items:
            reserve_task = item.task_set.get(flow_task=OrderItemFlow.reserve_item)
            response = self.client.post(
                f"/workflow/order/orderitem/{item.pk}"
                f"/reserve_item/{reserve_task.pk}/execute/",
                {"reserved": True, "_viewflow_activation-started": "2000-01-01"},
            )
            self.assertRedirects(response, f"/workflow/order/orderitem/{item.pk}/")

        for item in order_items:
            pack_task = item.task_set.get(flow_task=OrderItemFlow.pack_item)
            response = self.client.post(
                f"/workflow/order/orderitem/{item.pk}"
                f"/pack_item/{pack_task.pk}/execute/",
                {"_viewflow_activation-started": "2000-01-01"},
            )
            self.assertRedirects(response, f"/workflow/order/orderitem/{item.pk}/")

        self.assertTrue(
            all([process.status == "DONE" for process in Process.objects.all()])
        )
        self.assertEqual(18, Task.objects.count())


urlpatterns = [
    path("workflow/order/order/", FlowViewset(OrderFlow).urls),
    path("workflow/order/orderitem/", FlowViewset(OrderItemFlow).urls),
    path(
        "workflow/order/customerverification/",
        FlowViewset(CustomerVerificationFlow).urls,
    ),
]
