from django.conf.urls import url, include
from django.views import generic
from rest_framework.authtoken.views import obtain_auth_token
from viewflow.rest import views as rest

from hellorest.flows import HelloRestFlow


flows = {
    'helloworld': HelloRestFlow
}


urlpatterns = [
    url(r'^$', generic.TemplateView.as_view(template_name='index.html')),
    url(r'^login/$', obtain_auth_token),
    url(r'^flows/$', rest.FlowListView.as_view(ns_map=flows), name="flow-list"),
    url(r'^processes/$', rest.AllProcessListView.as_view(ns_map=flows), name="processe-list"),
    url(r'^tasks/$', rest.AllTaskListView.as_view(ns_map=flows), name="task-list"),

    url(r'^', include([
        url(r'^flows/hellorest/$',
            rest.DetailFlowView.as_view(), {'flow_class': HelloRestFlow}, name="flow"),
        url(r'^tasks/hellorest/', include([HelloRestFlow.instance.urls]))
    ], namespace='helloworld')),
]
