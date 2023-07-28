from django.apps import AppConfig


class CustomWidgetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cookbook.forms101.custom_widget"
