from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from viewflow.workflow.rest import FlowRestViewset
from .flows import HelloRestFlow


urlpatterns = [
    path("api/", get_schema_view(title="Workflow 101")),
    path(
        "api/swagger/",
        TemplateView.as_view(
            template_name="viewflow/contrib/swagger.html",
            extra_context={"api_url": "/api/"},
        ),
    ),
    path("api/hellorest/", FlowRestViewset(HelloRestFlow).urls),
]
