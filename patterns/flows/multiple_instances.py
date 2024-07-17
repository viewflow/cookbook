"""
Description:
    Within a process, multiple instances of a task can be created. These
    instances run independently and at the same time.

Example:
    When the Transport Department receives a list of traffic infringements, an
    Issue-Infringement-Notice task is created for each infringement on the list.

Purpose:
    Creating multiple instances of a task to process different data inputs
    simultaneously.
"""

from typing import List, TypedDict
from django import forms
from django.db.models import TextChoices
from viewflow import this, jsonstore
from viewflow.forms import FormSetField, Form, ModelForm
from viewflow.workflow import act, flow
from viewflow.workflow.flow import views
from viewflow.workflow.models import Process


class InfringementChoices(TextChoices):
    SPEEDING = "speeding", "Speeding"
    PARKING = "parking", "Illegal Parking"
    RED_LIGHT = "red_light", "Running a Red Light"
    NO_INSURANCE = "no_insurance", "No Insurance"
    NO_LICENSE = "no_license", "Driving Without a License"


class InfringementEntry(TypedDict):
    infringement: InfringementChoices


class InfringementProcess(Process):
    """Process model to store the traffic infringement details"""

    infringement_list: List[InfringementEntry] = jsonstore.JSONField(default=list)

    class Meta:
        proxy = True


class InfringementForm(Form):
    infringement = forms.ChoiceField(choices=InfringementChoices)


InfringementFormSet = forms.formset_factory(InfringementForm, can_delete=False, extra=3)


class InfringementListForm(ModelForm):
    infringements = FormSetField(InfringementFormSet)

    def save(self, commit=True):
        object = super().save(False)
        object.infringement_list = [
            data
            for data in self.formsets["infringements"].cleaned_data
            if data  # skip empty forms
        ]

        if commit:
            object.save()
        return object

    class Meta:
        model = InfringementProcess
        fields = []


class MultipleInstances(flow.Flow):
    start = (
        flow.Start(views.CreateProcessView.as_view(form_class=InfringementListForm))
        .Annotation(description="Select infringements")
        .Next(this.split_infringements)
    )

    split_infringements = (
        flow.Split()
        .Next(this.issue_notice, task_data_source=act.process.infringement_list)
        .Next(this.join_infringements)  # in case no infrigements added
    )

    issue_notice = (
        flow.Function(this.issue_notice_task)
        .Annotation(description="Issue Infringement Notice")
        .Next(this.join_infringements)
    )

    join_infringements = flow.Join().Next(this.end)

    end = flow.End()

    def issue_notice_task(self, activation):
        print(f"Notice for {activation.task.data['infringement']}")

    process_description = "Creating multiple instances of a task to process different data inputs simultaneously."

    def __str__(self) -> str:
        return (
            "When the Transport Department receives a list of traffic infringements, an "
            "Issue-Infringement-Notice task is created for each infringement on the list."
        )
