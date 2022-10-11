from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from . import models


@admin.register(models.Department)
class DepartmentAdmin(GuardedModelAdmin):
    list_display = ('name', 'description')
