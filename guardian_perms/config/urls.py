from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import path
from rest_framework.schemas import get_schema_view

from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Application, Site
from viewflow.workflow.rest import FlowRestViewset
from viewflow.workflow.flow import FlowAppViewset

from ..bills.flows import BillClearingFlow
from ..bills.viewsets import BillViewset, DepartmentViewset

site = Site(
    title="Guardian Permissions Demo",
    viewsets=[
        FlowAppViewset(
            BillClearingFlow,
            icon="request_quote",
            viewsets=[
                BillViewset(),
                DepartmentViewset(),
            ]
        ),
    ],
)


def users(request):
    return {
        'users': User.objects.filter(is_active=True).order_by('-username')
    }


def login_as(request):
    try:
        user = User.objects.get(username=request.GET.get('username'))
    except User.DoesNotExist:
        pass
    else:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    return redirect('/', status_code=303)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", AuthViewset().urls),
    path('login_as/', login_as, name="login_as"),
    path("api/", get_schema_view(title="Workflow 101")),
    path(
        "api/swagger/",
        TemplateView.as_view(
            template_name="viewflow/contrib/swagger.html",
            extra_context={"api_url": "/api/"},
        ),
    ),
    path("api/hellorest/", FlowRestViewset(HelloRestFlow).urls),
    path("", site.urls),
]
