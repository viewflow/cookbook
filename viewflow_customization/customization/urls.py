from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', TemplateView.as_view(template_name='login.html')),
    url(r'^parcel/', include('customization.parcel.urls')),
    url(r'^', include('customization.website')),
]
