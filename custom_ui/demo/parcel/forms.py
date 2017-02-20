from django import forms
from django.utils import timezone

from .models import DeliveryProcess


class ApproveForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(ApproveForm, self).save(commit=False)
        instance.approved_at = timezone.now()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = DeliveryProcess
        fields = ['approved']


class DropStatusForm(forms.ModelForm):
    class Meta:
        model = DeliveryProcess
        fields = ['drop_status']
        widgets = {
            'drop_status': forms.RadioSelect
        }
