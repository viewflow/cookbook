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
        self.assertRedirects(response, "/workflow/order/order/1/")

        response = self.client.post(
            "/workflow/order/customerverification/2/verify_customer/4/execute/",
            {"trusted": True, "_viewflow_activation-started": "2000-01-01"},
        )
        self.assertRedirects(response, "/workflow/order/customerverification/2/")

        response = self.client.post(
            "/workflow/order/orderitem/3/reserve_item/9/execute/",
            {"reserved": True, "_viewflow_activation-started": "2000-01-01"},
        )
        self.assertRedirects(response, "/workflow/order/orderitem/3/")

        response = self.client.post(
            "/workflow/order/orderitem/4/reserve_item/11/execute/",
            {"reserved": True, "_viewflow_activation-started": "2000-01-01"},
        )
        self.assertRedirects(response, "/workflow/order/orderitem/4/")

        response = self.client.post(
            "/workflow/order/orderitem/3/pack_item/13/execute/",
            {"_viewflow_activation-started": "2000-01-01"},
        )
        self.assertRedirects(response, "/workflow/order/orderitem/3/")

        response = self.client.post(
            "/workflow/order/orderitem/4/pack_item/15/execute/",
            {"_viewflow_activation-started": "2000-01-01"},
        )
        self.assertRedirects(response, "/workflow/order/orderitem/4/")

        self.assertTrue(
            all([process.status == "DONE" for process in Process.objects.all()])
        )
        self.assertEquals(18, Task.objects.count())


urlpatterns = [
    path("workflow/order/order/", FlowViewset(OrderFlow).urls),
    path("workflow/order/orderitem/", FlowViewset(OrderItemFlow).urls),
    path(
        "workflow/order/customerverification/",
        FlowViewset(CustomerVerificationFlow).urls,
    ),
]
