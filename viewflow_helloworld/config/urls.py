from django.contrib import admin
from django.views import generic
from django.conf.urls import url, include
from viewflow import views as viewflow
from helloworld.flows import HelloWorldFlow


urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(url='/helloworld/', permanent=False)),
    url('^admin/', include(admin.site.urls)),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^helloworld/', include([
        HelloWorldFlow.instance.urls,
        url('^$', viewflow.ProcessListView.as_view(), name='index'),
        url('^tasks/$', viewflow.TaskListView.as_view(), name='tasks'),
        url('^queue/$', viewflow.QueueListView.as_view(), name='queue'),
        url('^details/(?P<process_pk>\d+)/$', viewflow.ProcessDetailView.as_view(), name='details'),
    ], namespace=HelloWorldFlow.instance.namespace), {'flow_cls': HelloWorldFlow}),
]
