from django import forms
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView


class WizardForm1(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()


class WizardForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


class WizardView(SessionWizardView):
    form_list = [WizardForm1, WizardForm2]

    def done(self, form_list, **kwargs):
        return render(self.request, 'formtools/wizard/wizard_done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
