"""
Description
    This feature lets you decide later (at runtime) who will be assigned to
    complete a task, instead of deciding beforehand (at design time).

Example
    For the "Assess Damage" task, the person responsible is not decided until
    the process is running. At that time, a field called next_resource will be
    used to specify who should handle the task.

Motivation
    Deferred Distribution gives more flexibility by allowing the resource
    assignment for tasks to be delayed until runtime. This can be done by using
    a data field that holds the name of the person or group who should handle
    the task. The field's value can be updated during the process, which means
    the assignment can change dynamically as the process runs. This makes it
    easier to adapt to changes and manage tasks more efficiently.
"""

from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.forms import ModelForm, AjaxModelSelect
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process


class DamageAssessmentProcess(Process):
    damage_details = jsonstore.CharField(max_length=500)
    next_resource_id = jsonstore.IntegerField(null=True, blank=True)
    assessment_result = jsonstore.CharField(max_length=200, blank=True)

    @property
    def next_resource(self):
        if self.next_resource_id:
            return User.objects.get(id=self.next_resource_id)
        return None

    class Meta:
        proxy = True

    def __str__(self):
        return f"DamageAssessmentProcess: {self.damage_details[:50]}"


class DamageAssessmentForm(ModelForm):
    next_resource = ModelChoiceField(
        queryset=User.objects.all(),
        widget=AjaxModelSelect(lookups=["username__istartswith"]),
    )

    class Meta:
        model = DamageAssessmentProcess
        fields = ["damage_details"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if isinstance(self.cleaned_data["next_resource"], User):
            instance.next_resource_id = self.cleaned_data["next_resource"].id
        if commit:
            instance.save()
        return instance


class AssessmentResultForm(ModelForm):
    class Meta:
        model = DamageAssessmentProcess
        fields = ["assessment_result"]


class DeferredDistributionFlow(flow.Flow):
    process_class = DamageAssessmentProcess

    start = (
        flow.Start(CreateProcessView.as_view(form_class=DamageAssessmentForm))
        .Annotation(title="Submit Damage Details")
        .Permission(auto_create=True)
        .Next(this.assess_damage)
    )

    assess_damage = (
        flow.View(UpdateProcessView.as_view(form_class=AssessmentResultForm))
        .Annotation(title="Assess Damage")
        .Assign(lambda act: act.process.next_resource)
        .Next(this.end)
    )

    end = flow.End()

    process_description = (
        "This process allows damage details to be submitted, assigns a resource dynamically during runtime, "
        "and records the assessment result. The resource responsible for assessing the damage can be updated as needed."
    )

    def __str__(self):
        return "Deferred Distribution Flow"


class TestDeferredDistributionFlow(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.assessor = User.objects.create_user(
            username="assessor", password="password"
        )
        cls.reporter = User.objects.create_user(
            username="reporter", password="password"
        )

    def test_flow(self):
        self.client.login(username="reporter", password="password")

        # Start the process and submit damage details
        response = self.client.post(
            DeferredDistributionFlow.start.reverse("execute"),
            {
                "damage_details": "Minor scratches on the car",
                "next_resource_id": self.assessor.id,
            },
        )
        self.assertEqual(response.status_code, 302)

        # Assign resource (in this case, already set during the start)
        process = DamageAssessmentProcess.objects.get()
        self.assertEqual(process.next_resource, self.assessor)

        # Assessor logs in to handle the task
        self.client.login(username="assessor", password="password")
        assessment_task = process.task_set.get(
            flow_task=DeferredDistributionFlow.assess_damage
        )
        self.client.post(assessment_task.reverse("assign"), {})
        response = self.client.post(
            assessment_task.reverse("execute"),
            {"assessment_result": "Repaired in 2 hours"},
        )
        self.assertEqual(response.status_code, 302)

        # Verify the process completion
        process.refresh_from_db()
        self.assertEqual(process.assessment_result, "Repaired in 2 hours")
