from django.conf.urls import url, include
from django.views import generic
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from viewflow.rest import views as rest
from viewflow.rest.schemas import SchemaGenerator
from viewflow.rest.viewset import FlowViewSet

from hellorest.flows import HelloRestFlow


flows_nsmap = {
    'helloworld': HelloRestFlow
}

hello_urls = FlowViewSet(HelloRestFlow).urls


urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(url='/workflow/api/', permanent=False)),
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^workflow/api/$',
        get_schema_view(generator_class=SchemaGenerator),
        name='index'),
    url(r'^workflow/api/auth/token/$',
        obtain_auth_token,
        name='login'),
    url(r'^workflow/api/flows/$',
        rest.FlowListView.as_view(ns_map=flows_nsmap),
        name="flow-list"),
    url(r'^workflow/api/tasks/$',
        rest.AllTaskListView.as_view(ns_map=flows_nsmap),
        name="task-list"),

    url(r'^workflow/api/',
        include((hello_urls, 'helloworld'), namespace='helloworld')),
]
