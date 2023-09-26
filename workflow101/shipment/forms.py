from django import forms
from viewflow.forms import (
    ModelForm,
    InlineFormSetField,
    Layout,
    FieldSet,
    Row,
    Span,
    Tag,
    TotalCounterWidget,
)


from .models import Shipment, ShipmentItem


class ShipmentForm(ModelForm):
    items = InlineFormSetField(
        Shipment,
        ShipmentItem,
        fields=["name", "quantity"],
        can_delete=False,
        extra=1,
    )
    total = forms.CharField(
        widget=TotalCounterWidget(expression="sum(items.quantity)"), label=""
    )

    layout = Layout(
        Row("shipment_no"),
        FieldSet(
            "Customer Details", Row("first_name", "last_name", "email"), Row("phone")
        ),
        FieldSet(
            "Address",
            Row(Span("address", desktop=7), Span("zipcode", desktop=5)),
            Row(
                Span("city", desktop=5),
                Span("state", desktop=2),
                Span("country", desktop=5),
            ),
        ),
        "items",
        Row(
            Tag(
                "h4",
                text="Total:",
                style="text-align:right",
                class_="mdc-typography",
            ),
            "total",
        ),
    )

    class Meta:
        model = Shipment
        fields = [
            "shipment_no",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "zipcode",
            "city",
            "state",
            "country",
        ]
