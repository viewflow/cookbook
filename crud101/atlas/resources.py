from import_export import resources
from .models import City, Continent


class CityResource(resources.ModelResource):
    class Meta:
        model = City


class ContinentResource(resources.ModelResource):
    class Meta:
        model = Continent
