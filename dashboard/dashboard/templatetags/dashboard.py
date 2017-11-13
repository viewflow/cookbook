from django.apps import apps
from django.template import Library
from material.compat import simple_tag


register = Library()


def available_dashboards(context):
    user = context.request.user
    module = apps.get_app_config('dashboard')
    return [dashboard for dashboard in module.dashboards()
            if dashboard.has_perm(user)]



simple_tag(register, available_dashboards, takes_context=True)
