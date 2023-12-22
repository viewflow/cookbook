from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from viewflow.contrib.auth import AuthViewset
from viewflow.urls import ModelViewset, Site
from viewflow.workflow.flow.viewset import FlowAppViewset

from ..gptflow.flows import VideoBriefFlow
from ..gptflow.models import Article

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
