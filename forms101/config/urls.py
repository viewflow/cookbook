from django.contrib import admin
from django.urls import path
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site, Application

from ..forms.viewset import Forms
from ..custom_widget.viewset import EmailViewset, OrderViewset

site = Site(
    title="Material Forms Demo",
    viewsets=[
        Forms(),
        Application(
            viewsets=[EmailViewset(), OrderViewset()],
            app_name="widgets",
            title="Widgets",
        ),
    ],
)


urlpatterns = [
    path("accounts/", AuthViewset().urls),
    path("admin/", admin.site.urls),
    path("", site.urls),
]
