from django.urls import path
from viewflow.urls import Site
from viewflow.contrib.admin import Admin
from ..device_ops.viewset import DevicesDataApplication


site = Site(
    items=[
        DevicesDataApplication(),
        Admin(),
    ]
)

urlpatterns = [
    path('', site.urls),
]
