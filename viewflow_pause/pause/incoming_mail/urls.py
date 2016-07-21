from django.conf.urls import url
from viewflow.flow import views

from .flows import IncomingMailFlow
from .views import PausedListView


urlpatterns = [
    url('^$', views.ProcessListView.as_view(flow_cls=IncomingMailFlow), name='index'),
    url('^tasks/$', views.TaskListView.as_view(flow_cls=IncomingMailFlow), name='tasks'),
    url('^queue/$', views.QueueListView.as_view(flow_cls=IncomingMailFlow), name='queue'),
    url('^paused/$', PausedListView.as_view(flow_cls=IncomingMailFlow), name='paused'),
    url('^details/(?P<process_pk>\d+)/$',
        views.DetailProcessView.as_view(flow_cls=IncomingMailFlow), name='detail'),
    IncomingMailFlow.instance.urls,
]
