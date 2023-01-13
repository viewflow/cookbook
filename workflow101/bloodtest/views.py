from django.views import generic
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView

from viewflow.workflow.flow.views import mixins

from . import forms, models


class FirstBloodSampleView(mixins.TaskSuccessUrlMixin, SessionWizardView):
    template_name = "bloodtest/first_sample.html"

    form_list = [forms.PatientForm, forms.BloodSampleForm]

    def done(self, form_list, form_dict, **kwargs):
        patient = form_dict["0"].save()

        sample = form_dict["1"].save(commit=False)
        sample.patient = patient
        sample.taken_by = self.request.user
        sample.save()

        activation = self.request.activation
        activation.process.artifact = sample
        activation.execute()
        return redirect(self.get_success_url())


def second_blood_sample(request, **kwargs):
    form = forms.SecondBloodSampleForm(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.patient = form.cleaned_data["patient"]
        sample.taken_by = request.user
        sample.save()

        request.activation.process.artifact = sample
        request.activation.execute()
        return redirect(request.resolver_match.flow_viewset.get_success_url(request))

    return render(
        request,
        "bloodtest/second_sample.html",
        {"form": form, "activation": request.activation},
    )


def biochemical_data(request, **kwargs):
    form = forms.BiochemistryForm(request.POST or None)

    if form.is_valid():
        biochemistry = form.save(commit=False)
        biochemistry.sample = request.activation.process.artifact
        biochemistry.save()

        request.activation.execute()
        return redirect(request.resolver_match.flow_viewset.get_success_url(request))

    return render(
        request,
        "bloodtest/biochemical_data.html",
        {"form": form, "activation": request.activation},
    )


class HormoneTestFormView(mixins.TaskSuccessUrlMixin, generic.CreateView):
    model = models.Hormones
    fields = ["acth", "estradiol", "free_t3", "free_t4"]

    def form_valid(self, form):
        hormone_data = form.save(commit=False)
        hormone_data.sample = self.activation.process.sample
        hormone_data.save()

        self.request.activation.execute()
        return redirect(self.get_success_url())


class GenericTestFormView(mixins.TaskSuccessUrlMixin, generic.CreateView):
    """A generic view to save blood test data."""

    def form_valid(self, form):
        test_data = form.save(commit=False)
        test_data.sample = self.request.activation.process.artifact
        test_data.save()

        self.request.activation.execute()
        return redirect(self.get_success_url())
