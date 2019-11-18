from django.views import generic
from django.conf.urls import url, include


urlpatterns = [
    url('^$', generic.TemplateView.as_view(template_name='index.html')),
    url('^parcel/', include('demo.parcel.urls')),
    url('^accounts/', include('django.contrib.auth.urls')),
]
