from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from viewflow.contrib.admin import Admin
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site, Application
from ..orders.viewset import OrderViewset


site = Site(
    title="CRUD 101 Demo",
    primary_color="#3949ab",
    secondary_color="#5c6bc0",
    viewsets=[
        Application(
            icon="shopping_cart",
            viewsets=[OrderViewset()],
        ),
        Admin(),
    ],
)

urlpatterns = [
    path("", site.urls),
    path("accounts/", AuthViewset().urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
