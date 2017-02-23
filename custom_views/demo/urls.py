from django.conf.urls import url, include
from django.contrib import admin
from django.views import generic
from material.frontend import urls as frontend_urls


urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(url='/workflow/', permanent=False)),
    url(r'^admin/', admin.site.urls),
    url(r'', include(frontend_urls)),
]
