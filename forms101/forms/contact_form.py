from django import forms
from viewflow.forms import Layout, Row
from . import Form


class ContactForm(Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"leading-icon": "account_box"},
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"leading-icon": "email"},
        ),
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"leading-icon": "announcement"},
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
    )
    send_copy = forms.BooleanField(
        required=False,
        label="Send a copy to my e-mail address",
    )

    layout = Layout(
        Row("name", "email"),
        "subject",
        "message",
        "send_copy",
    )
