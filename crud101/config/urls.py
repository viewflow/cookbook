from django.urls import path
from viewflow.contrib.admin import Admin
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site
from ..atlas.viewset import atlas


site = Site(
    title="CRUD 101 Demo",
    primary_color='#3949ab',
    secondary_color='#5c6bc0',
    viewsets=[
        atlas,
        Admin(),
    ]
)

urlpatterns = [
    path('', site.urls),
    path('accounts/', AuthViewset().urls),
]
