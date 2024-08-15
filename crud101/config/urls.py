from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from viewflow.contrib.admin import Admin
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site, Application
from ..atlas.viewset import AtlasApp
from ..staff.urls import StaffApp
from ..tasks.viewsets import (
    TaskViewset,
    ProjectViewset,
    CategoryViewset,
    SubCategoryViewset,
)

site = Site(
    title="CRUD 101 Demo",
    primary_color="#3949ab",
    secondary_color="#5c6bc0",
    viewsets=[
        AtlasApp(),
        StaffApp(),
        Application(
            app_name="tasks",
            title="Tasks",
            icon="tasks",
            viewsets=[
                CategoryViewset(),
                SubCategoryViewset(),
                ProjectViewset(),
                TaskViewset(),
            ],
        ),
        Admin(),
    ],
)

urlpatterns = [
    path("", site.urls),
    path("accounts/", AuthViewset().urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
