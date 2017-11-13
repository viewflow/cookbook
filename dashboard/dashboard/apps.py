from django.apps import AppConfig
from django.template import Template, TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import autodiscover_modules

from material.frontend import ModuleURLResolver
from material.frontend.apps import ModuleMixin


class DashboardConfig(ModuleMixin, AppConfig):
    order = 1
    name = 'dashboard'
    icon = '<i class="material-icons">dashboard</i>'
    label = 'dashboard'
    verbose_name = _('Dashboard')

    def __init__(self, app_name, app_module):  # noqa D102
        super(DashboardConfig, self).__init__(app_name, app_module)
        self._registry = []

    def ready(self):
        """Import all <app>/dashboard.py modules."""
        autodiscover_modules('dashboard', register_to=self)

    def menu(self):
        """Module menu."""
        try:
            return get_template('dashboard/menu.html')
        except TemplateDoesNotExist:
            return Template('')

    def base_template(self):
        return get_template('dashboard/base_module.html')

    def register(self, dashboard):
        self._registry.append(dashboard)

    @property
    def registry(self):
        from .dashboard import default_dashboard

        if self._registry == []:
            return [default_dashboard]
        return self._registry

    def dashboards(self):
        registry = sorted(
            self.registry,
            key=lambda dashboard: force_text(dashboard.name))
        return registry

    def get_dashboard(self, dashboard_slug):
        for dashboard in self.registry:
            if dashboard.slug == dashboard_slug:
                return dashboard

    def has_perm(self, user):
        """True if there is at least one avaialble dashboard."""
        for dashboard in self.registry:
            if dashboard.has_perm(user):
                return True
        return False
