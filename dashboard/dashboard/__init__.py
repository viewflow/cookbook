from django.core.exceptions import ImproperlyConfigured

from .base import LayoutNode, Row, Column, Dashboard


__all__ = (
    'LayoutNode', 'Row', 'Column', 'Dashboard'
)


default_app_config = 'dashboard.apps.DashboardConfig'


def register(*args):
    from django.apps import apps
    module = apps.get_app_config('dashboard')

    if len(args) == 0:
        raise ImproperlyConfigured('No arguments provided')
    elif isinstance(args[0], Dashboard):
        module.register(args[0])
        if len(args) > 1:
            raise ImproperlyConfigured('Dashboard found. Rest arguments ignored')
    else:
        name, elements = args[0], args[1]
        module.register(Dashboard(name, elements))
