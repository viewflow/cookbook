from django.conf.urls import url, include
from viewflow.flow.viewset import FlowViewSet
from .flows import DeliveryFlow


delivery_urls = FlowViewSet(DeliveryFlow).urls

urlpatterns = [
     url(r'^delivery/', include(delivery_urls, namespace='delivery'))
]
