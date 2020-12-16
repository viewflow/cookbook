from django import forms
from viewflow.forms import Layout, Row, FormField, Form


class AddressForm(forms.Form):
    line_1 = forms.CharField(max_length=250)
    line_2 = forms.CharField(max_length=250)
    state = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=10)

    layout = Layout(
        'line_1',
        'line_2',
        'state',
        Row('city', 'zipcode'),
    )


class ProfileForm(Form):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    address = FormField(form_class=AddressForm)

    layout = Layout(
        'username',
        Row('first_name', 'last_name'),
        'address'
    )
