from django import forms
from viewflow.forms import Layout, Row, FormSetField, Form, Caption, FormSet


class EmailForm(forms.Form):
    email = forms.EmailField()
    description = forms.CharField()


class BaseEmailFormset(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        emails = []
        for form in self.forms:
            email = form.cleaned_data.get('email')
            if not email:
                continue
            if email in emails:
                raise forms.ValidationError("Emails should be distinct.")
            emails.append(email)


EmailFormSet = forms.formset_factory(EmailForm, extra=3, can_delete=True, formset=BaseEmailFormset)


class AddressForm(forms.Form):
    line_1 = forms.CharField(max_length=250)
    line_2 = forms.CharField(max_length=250)
    state = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=10)

    layout = Layout(
        Caption('Address'),
        'line_1',
        'line_2',
        'state',
        Row('city', 'zipcode'),
    )


AddressFormSet = forms.formset_factory(AddressForm, extra=3, can_delete=True)


class SignupForm(Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'leading-icon': 'account_box'}),
    )
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    date_of_birth = forms.DateField()
    emails = FormSetField(formset_class=EmailFormSet)
    addresses = FormSetField(formset_class=AddressFormSet)

    layout = Layout(
        'username',
        Row('first_name', 'last_name', 'date_of_birth'),
        'emails',
        FormSet('addresses', card_desktop=4),
    )
