from django import forms
from django.utils.translation import gettext_lazy as _


class StartOrderForm(forms.Form):
    """Collects the first line item so the order starts with something to do."""

    title = forms.CharField(label=_("First item"), max_length=150)


class AddItemForm(forms.Form):
    """Collects one more line item to spawn while the order is running."""

    title = forms.CharField(label=_("Item"), max_length=150)
