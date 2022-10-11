from viewflow.forms import ModelForm, InlineFormSetField, Layout, FieldSet, Row, Span


from .models import Shipment, ShipmentItem


class ShipmentForm(ModelForm):
    items = InlineFormSetField(
        Shipment, ShipmentItem, fields=["name", "quantity"], can_delete=False
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
