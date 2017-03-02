from django.contrib import admin

from .models import BillProcess


@admin.register(BillProcess)
class BillProcessAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assignment</i>'
    list_display = [
        'status', 'created', 'order_department',
        'accepted', 'signed', 'validated',
        'payment_date'
    ]
