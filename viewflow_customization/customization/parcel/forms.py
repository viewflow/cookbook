from django import forms
from . import models


class ParcelForm(forms.ModelForm):
    class Meta:
        model = models.Parcel
        fields = ['planet', 'description']


class ApproveForm(forms.ModelForm):
    class Meta:
        model = models.ShipmentProcess
        fields = ['approved']


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.ShipmentProcess
        fields = ['deliver_report']
