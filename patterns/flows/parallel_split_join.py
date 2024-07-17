"""
Pattern:
    One branch splits into two or more branches that run at the same time.

Example:
    After the customer pays, pack the goods and issue a receipt.

Purpose:
    The Parallel Split pattern allows one task to split into multiple tasks
    that run at the same time. These tasks can work together or separately.
    This improves the process by letting people and background tasks work on
    different parts at the same time.
"""

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.forms import ModelForm
from viewflow.workflow import flow, PROCESS
from viewflow.workflow.flow import views
from viewflow.workflow.models import Process


class OrderProcess(Process):
    order_id = jsonstore.CharField(max_length=50)
    packed = jsonstore.BooleanField(default=False)
    receipt_issued = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True


class ReceiptForm(ModelForm):
    class Meta:
        model = OrderProcess
        fields = ["receipt_issued"]
        widgets = {
            "receipt_issued": forms.CheckboxInput(attrs={"required": True}),
        }


class ParallelSplit(flow.Flow):
    process_class = OrderProcess

    start = (
        flow.Start(views.CreateProcessView.as_view(fields=["order_id"]))
        .Annotation(title="Start Order Process")
        .Permission(auto_create=True)
        .Next(this.split_payment_received)
    )

    split_payment_received = flow.Split().Next(this.pack_goods).Next(this.issue_receipt)

    pack_goods = (
        flow.View(views.UpdateProcessView.as_view(fields=["packed"]))
        .Annotation(title="Pack Goods")
        .Permission(auto_create=True)
        .Next(this.join)
    )

    issue_receipt = (
        flow.View(views.UpdateProcessView.as_view(form_class=ReceiptForm))
        .Annotation(title="Issue Receipt")
        .Permission(auto_create=True)
        .Next(this.join)
    )

    join = flow.Join().Next(this.end)

    end = flow.End()

    process_description = (
        "After the customer pays, pack the goods and issue a receipt. "
        "Continue, when both tasks are completed."
    )

    def __str__(self) -> str:
        return "One branch splits into two or more branches that run at the same time."


class Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(username="admin", password="admin")

    def test_first_order(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        # Start the process
        response = self.client.post(
            ParallelSplit.start.reverse("execute"), {"order_id": "12345"}
        )
        self.assertEqual(response.status_code, 302)

        process = OrderProcess.objects.get()
        process.task_set.get(flow_task=ParallelSplit.split_payment_received)

        # Simulate the task assignment and execution
        pack_task = process.task_set.get(flow_task=ParallelSplit.pack_goods)
        receipt_task = process.task_set.get(flow_task=ParallelSplit.issue_receipt)

        # Complete the pack_goods task
        response = self.client.post(pack_task.reverse("assign"), {})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(pack_task.reverse("execute"), {"packed": True})
        self.assertEqual(response.status_code, 302)

        # Complete the issue_receipt task
        response = self.client.post(receipt_task.reverse("assign"), {})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            receipt_task.reverse("execute"), {"receipt_issued": True}
        )
        self.assertEqual(response.status_code, 302)

        # Refresh the process and check if both tasks are completed
        process.refresh_from_db()
        self.assertEqual(process.status, PROCESS.DONE)
        self.assertTrue(process.packed)
        self.assertTrue(process.receipt_issued)

    def test_second_order(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        # Start the process
        response = self.client.post(
            ParallelSplit.start.reverse("execute"), {"order_id": "12345"}
        )
        self.assertEqual(response.status_code, 302)

        process = OrderProcess.objects.get()
        process.task_set.get(flow_task=ParallelSplit.split_payment_received)

        # Simulate the task assignment and execution
        pack_task = process.task_set.get(flow_task=ParallelSplit.pack_goods)
        receipt_task = process.task_set.get(flow_task=ParallelSplit.issue_receipt)

        # Complete the issue_receipt task
        response = self.client.post(receipt_task.reverse("assign"), {})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            receipt_task.reverse("execute"), {"receipt_issued": True}
        )
        self.assertEqual(response.status_code, 302)

        # Complete the pack_goods task
        response = self.client.post(pack_task.reverse("assign"), {})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(pack_task.reverse("execute"), {"packed": True})
        self.assertEqual(response.status_code, 302)

        # Refresh the process and check if both tasks are completed
        process.refresh_from_db()
        self.assertEqual(process.status, PROCESS.DONE)
        self.assertTrue(process.packed)
        self.assertTrue(process.receipt_issued)


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
            <bpmn:outgoing>id_edge_start__split_payment_received</bpmn:outgoing>
        </bpmn:startEvent>
        <bpmn:parallelGateway id="id_node_split_payment_received" >
            <bpmn:incoming>id_edge_start__split_payment_received</bpmn:incoming>
            <bpmn:outgoing>id_edge_split_payment_received__pack_goods</bpmn:outgoing>
            <bpmn:outgoing>id_edge_split_payment_received__issue_receipt</bpmn:outgoing>
        </bpmn:parallelGateway>
        <bpmn:userTask id="id_node_issue_receipt" name="Issue Receipt">
            <bpmn:incoming>id_edge_split_payment_received__issue_receipt</bpmn:incoming>
            <bpmn:outgoing>id_edge_issue_receipt__join</bpmn:outgoing>
        </bpmn:userTask>
        <bpmn:userTask id="id_node_pack_goods" name="Pack Goods">
            <bpmn:incoming>id_edge_split_payment_received__pack_goods</bpmn:incoming>
            <bpmn:outgoing>id_edge_pack_goods__join</bpmn:outgoing>
        </bpmn:userTask>
        <bpmn:parallelGateway id="id_node_join" >
            <bpmn:incoming>id_edge_issue_receipt__join</bpmn:incoming>
            <bpmn:incoming>id_edge_pack_goods__join</bpmn:incoming>
            <bpmn:outgoing>id_edge_join__end</bpmn:outgoing>
        </bpmn:parallelGateway>
        <bpmn:endEvent id="id_node_end" >
            <bpmn:incoming>id_edge_join__end</bpmn:incoming>
        </bpmn:endEvent>
        <bpmn:sequenceFlow id="id_edge_start__split_payment_received" sourceRef="id_node_start" targetRef="id_node_split_payment_received" />
        <bpmn:sequenceFlow id="id_edge_split_payment_received__issue_receipt" sourceRef="id_node_split_payment_received" targetRef="id_node_issue_receipt" />
        <bpmn:sequenceFlow id="id_edge_split_payment_received__pack_goods" sourceRef="id_node_split_payment_received" targetRef="id_node_pack_goods" />
        <bpmn:sequenceFlow id="id_edge_issue_receipt__join" sourceRef="id_node_issue_receipt" targetRef="id_node_join" />
        <bpmn:sequenceFlow id="id_edge_pack_goods__join" sourceRef="id_node_pack_goods" targetRef="id_node_join" />
        <bpmn:sequenceFlow id="id_edge_join__end" sourceRef="id_node_join" targetRef="id_node_end" />
    </bpmn:process>
    <bpmndi:BPMNDiagram>
        <bpmndi:BPMNPlane bpmnElement="id_process">
            <bpmndi:BPMNShape id="id_shape_start" bpmnElement="id_node_start">
                <dc:Bounds x="1" y="125" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_split_payment_received" bpmnElement="id_node_split_payment_received">
                <dc:Bounds x="75" y="125" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_issue_receipt" bpmnElement="id_node_issue_receipt">
                <dc:Bounds x="150" y="1" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_pack_goods" bpmnElement="id_node_pack_goods">
                <dc:Bounds x="150" y="200" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_join" bpmnElement="id_node_join">
                <dc:Bounds x="325" y="125" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_end" bpmnElement="id_node_end">
                <dc:Bounds x="400" y="125" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNEdge id="id_edge_shape_start__split_payment_received" bpmnElement="id_edge_start__split_payment_received" sourceElement="id_shape_start" targetElement="id_shape_split_payment_received">
                <di:waypoint xsi:type="dc:Point" x="51" y="150" />
                <di:waypoint xsi:type="dc:Point" x="75" y="150" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_split_payment_received__issue_receipt" bpmnElement="id_edge_split_payment_received__issue_receipt" sourceElement="id_shape_split_payment_received" targetElement="id_shape_issue_receipt">
                <di:waypoint xsi:type="dc:Point" x="100" y="125" />
                <di:waypoint xsi:type="dc:Point" x="100" y="51" />
                <di:waypoint xsi:type="dc:Point" x="150" y="51" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_split_payment_received__pack_goods" bpmnElement="id_edge_split_payment_received__pack_goods" sourceElement="id_shape_split_payment_received" targetElement="id_shape_pack_goods">
                <di:waypoint xsi:type="dc:Point" x="100" y="175" />
                <di:waypoint xsi:type="dc:Point" x="100" y="250" />
                <di:waypoint xsi:type="dc:Point" x="150" y="250" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_issue_receipt__join" bpmnElement="id_edge_issue_receipt__join" sourceElement="id_shape_issue_receipt" targetElement="id_shape_join">
                <di:waypoint xsi:type="dc:Point" x="300" y="51" />
                <di:waypoint xsi:type="dc:Point" x="350" y="51" />
                <di:waypoint xsi:type="dc:Point" x="350" y="125" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_pack_goods__join" bpmnElement="id_edge_pack_goods__join" sourceElement="id_shape_pack_goods" targetElement="id_shape_join">
                <di:waypoint xsi:type="dc:Point" x="300" y="250" />
                <di:waypoint xsi:type="dc:Point" x="350" y="250" />
                <di:waypoint xsi:type="dc:Point" x="350" y="175" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_join__end" bpmnElement="id_edge_join__end" sourceElement="id_shape_join" targetElement="id_shape_end">
                <di:waypoint xsi:type="dc:Point" x="375" y="150" />
                <di:waypoint xsi:type="dc:Point" x="400" y="150" />
            </bpmndi:BPMNEdge>
        </bpmndi:BPMNPlane>
    </bpmndi:BPMNDiagram>
</bpmn:definitions>
"""
