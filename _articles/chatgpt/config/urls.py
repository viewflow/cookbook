from django.contrib import admin
from django.urls import path
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site, ModelViewset
from viewflow.workflow.flow.viewset import FlowAppViewset
from ..gptflow.models import Article
from ..gptflow.flows import VideoBriefFlow

site = Site(
    title="Youtube Video Summary",
    viewsets=[
        FlowAppViewset(
            VideoBriefFlow,
            icon="video_library",
            viewsets=[
                ModelViewset(
                    model=Article,
                    list_columns=(
                        "pk",
                        "summary",
                        "created_at",
                    ),
                )
            ],
        )
    ],
)

urlpatterns = [
    path("accounts/", AuthViewset().urls),
    path("admin/", admin.site.urls),
    path("", site.urls),
]
