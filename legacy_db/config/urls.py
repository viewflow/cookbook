from django.urls import path
from viewflow.contrib.admin import Admin
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site
from ..airdata.viewset import AirportApp


site = Site(
    title="Airflights demo Database",
    primary_color='#3949ab',
    secondary_color='#5c6bc0',
    items=[
        AirportApp(),
        Admin(),
    ]
)

urlpatterns = [
    path('', site.urls),
    path('accounts/', AuthViewset().urls),
]
