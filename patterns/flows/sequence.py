"""
Pattern:
    A task starts only after the previous task in the same process is done.

Example:
    The verify-account task runs after the additinal user details are captured.

Purpose:
    The Sequence pattern is the basic building block for processes. It
    creates a series of tasks that run one after the other. Two tasks are in
    a Sequence if one directly follows the other without any conditions.

    Viewflow extracts workflow-related logic out of Django code, making it
    easier to manage.

    If tasks are data-independent, you can reorder them, place them in
    different parts of the workflow, run them in parallel, or reuse views
    and functions in different workflows.
"""

from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.forms import Layout, Row, Column, ModelForm, AjaxModelSelect
from viewflow.workflow import flow, PROCESS
from viewflow.workflow.flow.views import CreateProcessView
from viewflow.workflow.models import Process


class SequenceProcess(Process):
    seed: User
    birth_date = jsonstore.DateField(blank=True, null=True)
    marital_status = jsonstore.CharField(
        choices=[
            ("S", "Single"),
            ("M", "Married"),
            ("D", "Divorced"),
            ("W", "Widowed"),
        ],
    )
    bio = jsonstore.TextField(blank=True, default="")
    account_verified = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True


class SelectUserForm(ModelForm):
    seed = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="User",
    )

    class Meta:
        model = SequenceProcess
        fields = ["seed"]


class UserDetailsForm(ModelForm):
    layout = Layout(
        Row(Column("birth_date", "marital_status", desktop=4), "bio"),
    )

    class Meta:
        model = SequenceProcess
        fields = [
            "birth_date",
            "marital_status",
            "bio",
        ]


def input_user_details_view(request, **kwargs):
    form = UserDetailsForm(request.POST or None, instance=request.activation.process)
    if form.is_valid():
        form.save()

        # View is workflow independed and can be used in different flows.
        request.activation.execute()

        # Redirect to the next avaialbe task
        return redirect(request.activation.get_success_url(request))

    return render(request, "viewflow/workflow/task.html", {"form": form})


def verify_account(activation):
    """
    Do some script hard work here
    """
    activation.process.account_verified = True


class Sequence(flow.Flow):
    process_class = SequenceProcess

    start = flow.Start(CreateProcessView.as_view(form_class=SelectUserForm)).Next(
        this.input_user_details
    )

    input_user_details = flow.View(input_user_details_view).Next(this.verify_account)

    verify_account = flow.Function(verify_account).Next(this.end)

    end = flow.End()

    process_description = (
        "The verify-account task runs after the additinal user details are captured."
    )

    def __str__(self) -> str:
        return "A task starts only after the previous task in the same process is done."


class Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(username="admin", password="admin")

    def test_sequence_process(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        # start
        self.client.post(
            Sequence.start.reverse("execute"),
            {"seed": self.admin.pk},
        )

        process = SequenceProcess.objects.get()
        details = process.task_set.get(flow_task=Sequence.input_user_details)

        # input user details
        self.client.post(details.reverse("assign"), {})

        self.client.post(
            details.reverse("execute"),
            {"birth_date": "2001-01-01", "marital_status": "S", "bio": "test"},
        )

        # complete
        process.refresh_from_db()
        self.assertEqual(process.status, PROCESS.DONE)

        # verify_account executed after input_user_details
        verify = process.task_set.get(flow_task=Sequence.verify_account)
        self.assertEqual([details], list(verify.previous.all()))


BPMN = """
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
    xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
    xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
    targetNamespace="http://bpmn.io/schema/bpmn">
    <bpmn:process isExecutable="true" id="id_process">
        <bpmn:startEvent id="id_node_start" >
            <bpmn:outgoing>id_edge_start__input_user_details</bpmn:outgoing>
        </bpmn:startEvent>
        <bpmn:userTask id="id_node_input_user_details" name="Input User Details">
            <bpmn:incoming>id_edge_start__input_user_details</bpmn:incoming>
            <bpmn:outgoing>id_edge_input_user_details__verify_account</bpmn:outgoing>
        </bpmn:userTask>
        <bpmn:scriptTask id="id_node_verify_account" name="Verify Account">
            <bpmn:incoming>id_edge_input_user_details__verify_account</bpmn:incoming>
            <bpmn:outgoing>id_edge_verify_account__end</bpmn:outgoing>
        </bpmn:scriptTask>
        <bpmn:endEvent id="id_node_end" >
            <bpmn:incoming>id_edge_verify_account__end</bpmn:incoming>
        </bpmn:endEvent>
        <bpmn:sequenceFlow id="id_edge_start__input_user_details" sourceRef="id_node_start" targetRef="id_node_input_user_details" />
        <bpmn:sequenceFlow id="id_edge_input_user_details__verify_account" sourceRef="id_node_input_user_details" targetRef="id_node_verify_account" />
        <bpmn:sequenceFlow id="id_edge_verify_account__end" sourceRef="id_node_verify_account" targetRef="id_node_end" />
    </bpmn:process>
    <bpmndi:BPMNDiagram>
        <bpmndi:BPMNPlane bpmnElement="id_process">
            <bpmndi:BPMNShape id="id_shape_start" bpmnElement="id_node_start">
                <dc:Bounds x="1" y="25" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_input_user_details" bpmnElement="id_node_input_user_details">
                <dc:Bounds x="75" y="1" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_verify_account" bpmnElement="id_node_verify_account">
                <dc:Bounds x="250" y="1" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_end" bpmnElement="id_node_end">
                <dc:Bounds x="425" y="25" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNEdge id="id_edge_shape_start__input_user_details" bpmnElement="id_edge_start__input_user_details" sourceElement="id_shape_start" targetElement="id_shape_input_user_details">
                <di:waypoint xsi:type="dc:Point" x="51" y="50" />
                <di:waypoint xsi:type="dc:Point" x="75" y="51" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_input_user_details__verify_account" bpmnElement="id_edge_input_user_details__verify_account" sourceElement="id_shape_input_user_details" targetElement="id_shape_verify_account">
                <di:waypoint xsi:type="dc:Point" x="225" y="51" />
                <di:waypoint xsi:type="dc:Point" x="250" y="51" />
            </bpmndi:BPMNEdge>            
            <bpmndi:BPMNEdge id="id_edge_shape_verify_account__end" bpmnElement="id_edge_verify_account__end" sourceElement="id_shape_verify_account" targetElement="id_shape_end">                
                <di:waypoint xsi:type="dc:Point" x="400" y="51" />                
                <di:waypoint xsi:type="dc:Point" x="425" y="50" />                
            </bpmndi:BPMNEdge>            
        </bpmndi:BPMNPlane>
    </bpmndi:BPMNDiagram>
</bpmn:definitions>
"""
