from viewflow.urls import Application
from . import viewsets


class SalesApp(Application):
    title = "CRM"
    icon = "people"
    app_name = "crm"
    viewsets = [
        viewsets.CustomerViewset(),
        viewsets.ContactViewset(),
        viewsets.SaleViewset(),
    ]
