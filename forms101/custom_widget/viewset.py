from viewflow.urls import ModelViewset
from . import models, forms


class EmailViewset(ModelViewset):
    model = models.Email
    list_columns = ("pk", "sent_at", "subject", "from_email", "to_email")
    form_class = forms.EmailForm


class OrderViewset(ModelViewset):
    model = models.Order
    list_columns = (
        "customer_name",
        "quantity",
        "unit_price",
    )
    form_class = forms.OrderForm
