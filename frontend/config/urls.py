from django.contrib import admin
from django.urls import path, include
from django.views import generic
from material.frontend import urls as frontend_urls


urlpatterns = [
    path('', generic.RedirectView.as_view(url='/sales/', permanent=False)),
    path('', include(frontend_urls)),
    path('admin/', admin.site.urls),
]
