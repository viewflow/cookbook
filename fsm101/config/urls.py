from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from viewflow.workflow.rest.views import get_schema_view

from cookbook.fsm101.review.rest import ReviewViewSet


router = routers.DefaultRouter()
router.register(r"review", ReviewViewSet)


urlpatterns = [
    path("api/swagger/", TemplateView.as_view(template_name="review/api.html")),
    path("api/", get_schema_view(title="FSM 101")),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
