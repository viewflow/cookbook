from django import forms
from material import Layout, Row, Span2

from . import models


class PatientForm(forms.ModelForm):
    layout = Layout(
        Row(Span2('patient_id'), 'age', 'sex'),
        Row('weight', 'height'),
        'comment',
    )

    class Meta:
        model = models.Patient
        fields = '__all__'


class BloodSampleForm(forms.ModelForm):
    class Meta:
        model = models.BloodSample
        fields = ['taken_at', 'notes']


class BiochemistryForm(forms.ModelForm):
    class Meta:
        model = models.Biochemistry
        fields = ['hemoglobin', 'lymphocytes']


class SecondBloodSampleForm(BloodSampleForm):
    patient = forms.ModelChoiceField(queryset=models.Patient.objects.all())
