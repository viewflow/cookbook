from django.contrib import admin
from django.views import generic
from django.conf.urls import url, include
from material.frontend import urls as frontend_urls


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='/dashboard/', permanent=False)),
    url('^admin/', admin.site.urls),
    url(r'', include(frontend_urls)),
]
