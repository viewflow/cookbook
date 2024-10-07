from django.contrib import admin
from . import models


@admin.register(models.Sale)
class SaleAdmin(admin.ModelAdmin):
    pass
