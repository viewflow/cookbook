from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class SalesConfig(ModuleMixin, AppConfig):
    name = 'sales'
    icon = '<i class="material-icons">flight_takeoff</i>'
