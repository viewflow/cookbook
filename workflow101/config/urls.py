from django.urls import path

from viewflow import Icon
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site
from viewflow.workflow.flow import FlowAppViewset

from ..helloworld.flows import HelloWorldFlow


site = Site(title="Workflow 101 Demo", viewsets=[
    FlowAppViewset(HelloWorldFlow, icon=Icon('assignment')),
])


urlpatterns = [
    path('accounts/', AuthViewset().urls),
    path('', site.urls),
]
