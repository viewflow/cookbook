from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('data', )
    exclude = ['content_type', 'data']


@admin.register(models.Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'salary', 'department']
    fieldsets = UserAdmin.fieldsets + (
        ("Employee data", {'fields': ('hire_date', 'salary', 'department')}),
    )


@admin.register(models.Client)
class ClientAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'city')
    list_filter = ('vip', )
    fieldsets = UserAdmin.fieldsets + (
        ("Client data", {'fields': ('address', 'zip_code', 'city', 'vip')}),
    )
