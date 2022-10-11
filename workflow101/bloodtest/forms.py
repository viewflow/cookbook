from django import forms
from viewflow.forms import Layout, Row, Span

from . import models


class PatientForm(forms.ModelForm):
    layout = Layout(
        Row(Span("patient_id", desktop=2), "age", "sex"),
        Row("weight", "height"),
        "comment",
    )

    class Meta:
        model = models.Patient
        fields = "__all__"


class BloodSampleForm(forms.ModelForm):
    class Meta:
        model = models.BloodSample
        fields = ["taken_at", "notes"]


class BiochemistryForm(forms.ModelForm):
    class Meta:
        model = models.Biochemistry
        fields = ["hemoglobin", "lymphocytes"]


class SecondBloodSampleForm(BloodSampleForm):
    patient = forms.ModelChoiceField(queryset=models.Patient.objects.all())
