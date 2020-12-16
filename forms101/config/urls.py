from django.contrib import admin
from django.urls import path
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site

from ..forms.viewset import Forms


site = Site(title="Material Forms Demo", items=[
    Forms(),
])


urlpatterns = [
    path('accounts/', AuthViewset().urls),
    path('admin/', admin.site.urls),
    path('', site.urls),
]
