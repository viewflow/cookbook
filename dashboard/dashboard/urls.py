from django.conf.urls import url

from . import views

urlpatterns = [
        url('^$', views.default_dashboard, name="index"),
        url('^(?P<slug>[-\w]+)/$', views.dashboard, name="dashboard"),
]
