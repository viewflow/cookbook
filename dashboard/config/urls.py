from django.urls import path
from viewflow.contrib.admin import Admin
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site, Application

from cookbook.dashboard.board.views import dashboard_view

site = Site(
    title="CRUD 101 Demo",
    primary_color='#3949ab',
    secondary_color='#5c6bc0',
    viewsets=[
        Application(
            title='Dashboard',
            menu_template_name='board/app_menu.html',
            urls=[
                path('', dashboard_view, name='index')
            ]
        ),
        Admin(),
    ]
)

urlpatterns = [
    path('', site.urls),
    path('accounts/', AuthViewset().urls),
]
