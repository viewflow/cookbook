from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class SampleAppConfig(ModuleMixin, AppConfig):
    name = 'sample_app'
    icon = '<i class="material-icons">extension</i>'
