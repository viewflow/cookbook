from viewflow.urls import ReadonlyModelViewset, ModelViewset
from . import models


class ShipmentViewset(ReadonlyModelViewset):
    model = models.Shipment
    icon = 'local_post_office'


class CarierViewset(ModelViewset):
    model = models.Carrier
    icon = 'airport_shuttle'
