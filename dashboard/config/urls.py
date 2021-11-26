from django.urls import path
from viewflow.contrib.admin import Admin
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site, Application

from ..oilngas.dashboard import dashboard as oilDashboard
from ..stocks.dashboard import dashboard as stocksDashboard
from ..tests.dashboard import dashboard
from ..django_stats import DjangoStatsDashboard


site = Site(
    title="CRUD 101 Demo",
    primary_color='#3949ab',
    secondary_color='#5c6bc0',
    viewsets=[
        Application(
            title='Dashboard',
            viewsets=[
                oilDashboard,
                stocksDashboard,
                DjangoStatsDashboard(),
                dashboard,
            ]
        ),
        Admin(),
    ]
)

urlpatterns = [
    path('', site.urls),
    path('accounts/', AuthViewset().urls),
]
