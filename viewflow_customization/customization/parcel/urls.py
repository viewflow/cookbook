from django.conf.urls import patterns, include, url

from . import views, flows


urlpatterns = patterns(
    '',
    url(r'^list/', views.process_list, name="parcels"),
    url(r'^tasks/', views.task_list, name="tasks"),
    url(r'^details/(?P<process_pk>\d+)/', views.details, name="details"),
    url(r'^',
        include([flows.ShipmentFlow.instance.urls], namespace=flows.ShipmentFlow.instance.namespace),
        {'flow_cls': flows.ShipmentFlow})
)
