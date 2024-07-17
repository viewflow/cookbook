"""
Pattern:
    One branch splits into two or more branches, but only one branch is
    chosen to continue based on certain criteria.

Example:
    After the review election task, either declare results or recount votes.

Purpose:
    The Exclusive Choice pattern directs the process to a specific task
    based on the outcome of a previous task, data values, or a programmatic
    selection. This decision is made dynamically at runtime.
"""

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.forms import ModelForm, Layout, FieldSet, Row, Span
from viewflow.workflow import act, flow, PROCESS
from viewflow.workflow.models import Process
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView


class ElectionProcess(Process):
    title = jsonstore.CharField(max_length=250)
    description = jsonstore.CharField(max_length=1000, blank=True)
    recount_votes = jsonstore.BooleanField(
        default=False, choices=((1, "Yes"), (0, "No"))
    )

    class Meta:
        proxy = True


class ElectionForm(ModelForm):
    class Meta:
        model = ElectionProcess
        fields = ["title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    layout = Layout(
        FieldSet(
            "Election Details",
            Row(Span("title", desktop=4), Span("description", desktop=8)),
        ),
    )


class DecisionForm(ModelForm):
    class Meta:
        model = ElectionProcess
        fields = ["recount_votes"]
        widgets = {"recount_votes": forms.RadioSelect()}


class ExclusiveChoice(flow.Flow):
    process_class = ElectionProcess

    start = (
        flow.Start(CreateProcessView.as_view(form_class=ElectionForm))
        .Annotation(title="Start Election Process")
        .Permission(auto_create=True)
        .Next(this.review_election)
    )

    review_election = (
        flow.View(UpdateProcessView.as_view(form_class=DecisionForm))
        .Annotation(title="Review Election")
        .Next(this.choose_action)
    )

    choose_action = (
        flow.If(act.process.recount_votes)
        .Annotation(title="Choose Action")
        .Then(this.recount)
        .Else(this.declare)
    )

    recount = (
        flow.Function(this.recount_votes_action)
        .Annotation(title="Recount Votes")
        .Next(this.end)
    )

    declare = (
        flow.Function(this.declare_results_action)
        .Annotation(title="Declare Results")
        .Next(this.end)
    )

    end = flow.End()

    def recount_votes_action(self, activation):
        # Implement recount votes logic here
        pass

    def declare_results_action(self, activation):
        # Implement declare results logic here
        pass

    process_description = (
        "After the review election task, either declare results or recount votes."
    )

    def __str__(self) -> str:
        return (
            "One branch splits into two or more branches, but only one branch is "
            "chosen to continue based on certain criteria."
        )


class Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(username="admin", password="admin")

    def test_first_branch(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        # start
        self.client.post(
            ExclusiveChoice.start.reverse("execute"),
            {"title": "Test", "description": "Sample paper"},
        )

        process = ElectionProcess.objects.get()
        review = process.task_set.get(flow_task=ExclusiveChoice.review_election)

        # input user details
        self.client.post(review.reverse("assign"), {})

        self.client.post(
            review.reverse("execute"),
            {"recount_votes": "1"},
        )

        # complete
        process.refresh_from_db()
        self.assertEqual(process.status, PROCESS.DONE)
        process.task_set.get(flow_task=ExclusiveChoice.recount)

    def test_second_branch(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        # start
        self.client.post(
            ExclusiveChoice.start.reverse("execute"),
            {"title": "Test", "description": "Sample paper"},
        )

        process = ElectionProcess.objects.get()
        review = process.task_set.get(flow_task=ExclusiveChoice.review_election)

        # input user details
        self.client.post(review.reverse("assign"), {})

        self.client.post(
            review.reverse("execute"),
            {"recount_votes": "0"},
        )

        # complete
        process.refresh_from_db()
        self.assertEqual(process.status, PROCESS.DONE)
        process.task_set.get(flow_task=ExclusiveChoice.declare)


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
            <bpmn:outgoing>id_edge_start__review_election</bpmn:outgoing>
        </bpmn:startEvent>
        <bpmn:userTask id="id_node_review_election" name="Review Election">
            <bpmn:incoming>id_edge_start__review_election</bpmn:incoming>
            <bpmn:outgoing>id_edge_review_election__choose_action</bpmn:outgoing>
        </bpmn:userTask>
        <bpmn:exclusiveGateway id="id_node_choose_action" >
            <bpmn:incoming>id_edge_review_election__choose_action</bpmn:incoming>
            <bpmn:outgoing>id_edge_choose_action__recount</bpmn:outgoing>
            <bpmn:outgoing>id_edge_choose_action__declare</bpmn:outgoing>
        </bpmn:exclusiveGateway>
        <bpmn:scriptTask id="id_node_declare" name="Declare Results">
            <bpmn:incoming>id_edge_choose_action__declare</bpmn:incoming>
            <bpmn:outgoing>id_edge_declare__end</bpmn:outgoing>
        </bpmn:scriptTask>
        <bpmn:scriptTask id="id_node_recount" name="Recount Votes">
            <bpmn:incoming>id_edge_choose_action__recount</bpmn:incoming>
            <bpmn:outgoing>id_edge_recount__end</bpmn:outgoing>
        </bpmn:scriptTask>
        <bpmn:endEvent id="id_node_end" >
            <bpmn:incoming>id_edge_declare__end</bpmn:incoming>
            <bpmn:incoming>id_edge_recount__end</bpmn:incoming>
        </bpmn:endEvent>
        <bpmn:sequenceFlow id="id_edge_start__review_election" sourceRef="id_node_start" targetRef="id_node_review_election" />
        <bpmn:sequenceFlow id="id_edge_review_election__choose_action" sourceRef="id_node_review_election" targetRef="id_node_choose_action" />
        <bpmn:sequenceFlow id="id_edge_choose_action__declare" sourceRef="id_node_choose_action" targetRef="id_node_declare" />
        <bpmn:sequenceFlow id="id_edge_choose_action__recount" sourceRef="id_node_choose_action" targetRef="id_node_recount" />
        <bpmn:sequenceFlow id="id_edge_declare__end" sourceRef="id_node_declare" targetRef="id_node_end" />
        <bpmn:sequenceFlow id="id_edge_recount__end" sourceRef="id_node_recount" targetRef="id_node_end" />
    </bpmn:process>
    <bpmndi:BPMNDiagram>
        <bpmndi:BPMNPlane bpmnElement="id_process">
            <bpmndi:BPMNShape id="id_shape_start" bpmnElement="id_node_start">
                <dc:Bounds x="1" y="150" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_review_election" bpmnElement="id_node_review_election">
                <dc:Bounds x="75" y="125" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_choose_action" bpmnElement="id_node_choose_action">
                <dc:Bounds x="250" y="150" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_declare" bpmnElement="id_node_declare">
                <dc:Bounds x="325" y="1" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_recount" bpmnElement="id_node_recount">
                <dc:Bounds x="325" y="250" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_end" bpmnElement="id_node_end">
                <dc:Bounds x="500" y="150" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNEdge id="id_edge_shape_start__review_election" bpmnElement="id_edge_start__review_election" sourceElement="id_shape_start" targetElement="id_shape_review_election">
                <di:waypoint xsi:type="dc:Point" x="51" y="175" />
                <di:waypoint xsi:type="dc:Point" x="75" y="175" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_review_election__choose_action" bpmnElement="id_edge_review_election__choose_action" sourceElement="id_shape_review_election" targetElement="id_shape_choose_action">
                <di:waypoint xsi:type="dc:Point" x="225" y="175" />
                <di:waypoint xsi:type="dc:Point" x="250" y="175" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_choose_action__declare" bpmnElement="id_edge_choose_action__declare" sourceElement="id_shape_choose_action" targetElement="id_shape_declare">
                <di:waypoint xsi:type="dc:Point" x="275" y="150" />
                <di:waypoint xsi:type="dc:Point" x="275" y="51" />
                <di:waypoint xsi:type="dc:Point" x="325" y="51" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_choose_action__recount" bpmnElement="id_edge_choose_action__recount" sourceElement="id_shape_choose_action" targetElement="id_shape_recount">
                <di:waypoint xsi:type="dc:Point" x="275" y="200" />
                <di:waypoint xsi:type="dc:Point" x="275" y="300" />
                <di:waypoint xsi:type="dc:Point" x="325" y="300" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_declare__end" bpmnElement="id_edge_declare__end" sourceElement="id_shape_declare" targetElement="id_shape_end">
                <di:waypoint xsi:type="dc:Point" x="475" y="51" />
                <di:waypoint xsi:type="dc:Point" x="525" y="51" />
                <di:waypoint xsi:type="dc:Point" x="525" y="150" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_recount__end" bpmnElement="id_edge_recount__end" sourceElement="id_shape_recount" targetElement="id_shape_end">
                <di:waypoint xsi:type="dc:Point" x="475" y="300" />
                <di:waypoint xsi:type="dc:Point" x="525" y="300" />
                <di:waypoint xsi:type="dc:Point" x="525" y="200" />
            </bpmndi:BPMNEdge>
        </bpmndi:BPMNPlane>
    </bpmndi:BPMNDiagram>
</bpmn:definitions>
"""
