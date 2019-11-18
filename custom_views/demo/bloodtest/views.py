from django.views import generic
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView

from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.flow.views.utils import get_next_task_url

from . import forms, models


class FirstBloodSampleView(StartFlowMixin, SessionWizardView):
    template_name = 'bloodtest/bloodtest/first_sample.html'

    form_list = [forms.PatientForm, forms.BloodSampleForm]

    def done(self, form_list, form_dict, **kwargs):
        patient = form_dict['0'].save()

        sample = form_dict['1'].save(commit=False)
        sample.patient = patient
        sample.taken_by = self.request.user
        sample.save()

        self.activation.process.sample = sample
        self.activation.done()

        return redirect(get_next_task_url(self.request, self.activation.process))


@flow_start_view
def second_blood_sample(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.SecondBloodSampleForm(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.patient = form.cleaned_data['patient']
        sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'bloodtest/bloodtest/second_sample.html', {
        'form': form,
        'activation': request.activation
    })


@flow_view
def biochemical_data(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.BiochemistryForm(request.POST or None)

    if form.is_valid():
        biochemestry = form.save(commit=False)
        biochemestry.sample = request.activation.process.sample
        biochemestry.save()
        request.activation.done()
        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'bloodtest/bloodtest/biochemical_data.html', {
        'form': form,
        'activation': request.activation
    })


class HormoneTestFormView(FlowMixin, generic.CreateView):
    template_name = 'bloodtest/bloodtest/hormone_data.html'
    model = models.Hormones
    fields = [
        'acth', 'estradiol', 'free_t3', 'free_t4'
    ]

    def form_valid(self, form):
        hormone_data = form.save(commit=False)
        hormone_data.sample = self.activation.process.sample
        hormone_data.save()
        self.activation_done()
        return redirect(self.get_success_url())


class GenericTestFormView(FlowMixin, generic.CreateView):
    """A generic view to save blood test data.

    Assumes that test data model have FK `sample` field. The view can
    be parametrized directly in flow definition.

    """
    def form_valid(self, form):
        test_data = form.save(commit=False)
        test_data.sample = self.activation.process.sample
        test_data.save()
        self.activation_done()
        return redirect(self.get_success_url())
