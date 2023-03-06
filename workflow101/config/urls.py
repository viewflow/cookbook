from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import path, include

from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Application, Site
from viewflow.workflow.flow import FlowAppViewset

from ..bloodtest.flows import BloodTestFlow
from ..dynamic_split.flows import DynamicSplitFlow
from ..helloworld.flows import HelloWorldFlow
from ..shipment.flows import ShipmentFlow
from ..shipment.viewsets import ShipmentViewset, CarierViewset
from ..subprocess.flows import OrderItemFlow, CustomerVerificationFlow, OrderFlow

site = Site(
    title="Workflow 101 Demo",
    viewsets=[
        Application(
            app_name="intro",
            icon="account_balance",
            title="Introduction",
            menu_template_name=None,
            urlpatterns=[
                path(
                    "",
                    TemplateView.as_view(template_name="workflow101/index.html"),
                    name="index",
                ),
            ],
        ),
        FlowAppViewset(HelloWorldFlow, icon="assignment"),
        FlowAppViewset(DynamicSplitFlow, icon="call_split"),
        FlowAppViewset(BloodTestFlow, icon="bloodtype"),
        Site(
            app_name="subprocess",
            title="Orders processing",
            icon="account_tree",
            permission="view_orderprocess",
            primary_color="#d20011",
            viewsets=[
                FlowAppViewset(OrderFlow, icon="shopping_cart"),
                FlowAppViewset(CustomerVerificationFlow, icon="hail"),
                FlowAppViewset(OrderItemFlow, icon="toc"),
                FlowAppViewset(
                    ShipmentFlow,
                    icon="local_shipping",
                    viewsets=[
                        CarierViewset(),
                        ShipmentViewset(),
                    ],
                ),
            ],
        ),
    ],
)


def users(request):
    return {"users": User.objects.filter(is_active=True).order_by("-username")}


def login_as(request):
    try:
        user = User.objects.get(username=request.GET.get("username"))
    except User.DoesNotExist:
        pass
    else:
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
    return redirect("/")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", AuthViewset().urls),
    path("login_as/", login_as, name="login_as"),
    path("", include("cookbook.workflow101.hellorest.urls")),
    path("", site.urls),
]
