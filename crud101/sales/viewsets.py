from viewflow.forms import AjaxModelSelect, DependentModelSelect
from viewflow.urls import ModelViewset

from . import models


class CustomerViewset(ModelViewset):
    model = models.Customer
    list_columns = ["name"]


class ContactViewset(ModelViewset):
    model = models.Contact
    list_columns = ["email", "phone_number", "is_primary"]
    list_filter_fields = ["is_primary", "customer"]


class SaleViewset(ModelViewset):
    model = models.Sale
    list_columns = ["sale_amount", "sale_date", "customer", "primary_contact"]
    list_filter_fields = ["sale_date", "customer"]
    form_widgets = {
        "primary_contact": DependentModelSelect(
            depends_on="customer", queryset=lambda customer: customer.contacts
        ),
        "customer": AjaxModelSelect(
            lookups=["name__istartswith"],
        ),
    }
