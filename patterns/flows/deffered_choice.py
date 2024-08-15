"""
Description: 
    At a certain point in a process, a decision is made to follow one path out
    of several options. Before the decision, all paths are open. The choice is
    made by starting the first task in one path, creating a race between them.
    Once a path is chosen, the others are stopped.

Examples:
    In the Resolve complaint process, there's a choice between starting with the
    Initial customer contact or escalating to a manager. The Initial customer
    contact begins when a customer service team member starts it. If not
    started, the Escalate to manager task begins after 48 hours. Once one task
    starts, the other stops.

Purpose:
    The Deferred Choice pattern delays deciding which path to take until it's
    necessary. The decision depends on external factors like messages, data from
    the environment, resource availability, or time limits. Until the decision
    is made, any path could be chosen.
"""

import time
from unittest.mock import patch
from django.contrib.auth.models import User

from viewflow import this, jsonstore
from viewflow.contrib import celery
from viewflow.workflow import flow, STATUS
from viewflow.workflow.models import Process
from viewflow.workflow.flow import views

try:
    from tests.contrib import CeleryTestCase
except ImportError:
    # just fallback on deployment without tests
    from django.test import TestCase as CeleryTestCase


class DeferredChoiceProcess(Process):
    text = jsonstore.CharField(max_length=150)
    customer_contacted = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True


class DefferedChoice(flow.Flow):
    process_class = DeferredChoiceProcess

    start = (
        flow.Start(views.CreateProcessView.as_view(fields=["text"]))
        .Annotation(title="New Complaint")
        .Permission(auto_create=True)
        .Next(this.split_first)
    )

    split_first = flow.SplitFirst().Next(this.initial_customer_contact).Next(this.timer)

    initial_customer_contact = (
        flow.View(views.UpdateProcessView.as_view(fields=["customer_contacted"]))
        .Annotation(title="Initial Customer Contact")
        .Permission(auto_create=True)
        .Next(this.join)
    )

    timer = celery.Timer(2 * 60).Next(this.manager_contact)

    manager_contact = flow.Function(this.escalate_to_manager).Next(this.join)

    join = flow.Join().Next(this.end)

    end = flow.End()

    def escalate_to_manager(self, activation):
        print("Escalate to manager")

    process_description = "Resolve complaints via customer contact or escalate after 2 minutes of inactivity."

    def __str__(self) -> str:
        return (
            "At a decision point in a process, one path is chosen from several options by "
            "starting the first task, stopping others once a path is selected."
        )


class Test(CeleryTestCase):
    SETTINGS = "cookbook.patterns.config"

    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="admin")
        super().setUp()

    def test_timer_executed_first(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        with patch.object(DefferedChoice.timer, "_delay", 4):
            # Start the process
            response = self.client.post(
                DefferedChoice.start.reverse("execute"), {"text": "test"}
            )
            self.assertEqual(response.status_code, 302)
            process = DeferredChoiceProcess.objects.get()
            self.wait_for_task(process, DefferedChoice.timer, STATUS.DONE)

        process.refresh_from_db()

        self.assertEqual(STATUS.DONE, process.status)
        self.assertEqual(
            STATUS.CANCELED,
            process.task_set.get(
                flow_task=DefferedChoice.initial_customer_contact
            ).status,
        )
        self.assertEqual(
            STATUS.DONE,
            process.task_set.get(flow_task=DefferedChoice.manager_contact).status,
        )

    def test_initial_contact_executed_first(self):
        self.assertTrue(self.client.login(username="admin", password="admin"))

        with patch.object(DefferedChoice.timer, "_delay", 3):
            response = self.client.post(
                DefferedChoice.start.reverse("execute"), {"text": "test"}
            )
            self.assertEqual(response.status_code, 302)
            process = DeferredChoiceProcess.objects.get()

            contact_task = process.task_set.get(
                flow_task=DefferedChoice.initial_customer_contact
            )

            response = self.client.post(contact_task.reverse("assign"), {})
            self.assertEqual(response.status_code, 302)
            response = self.client.post(contact_task.reverse("execute"), {})
            self.assertEqual(response.status_code, 302)

            process.refresh_from_db()

        self.assertEqual(STATUS.DONE, process.status)
        self.assertEqual(
            STATUS.DONE,
            process.task_set.get(
                flow_task=DefferedChoice.initial_customer_contact
            ).status,
        )
        self.assertEqual(
            STATUS.CANCELED,
            process.task_set.get(flow_task=DefferedChoice.timer).status,
        )

        time.sleep(4)  # wait for timer task been canceld on celery


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
            <bpmn:outgoing>id_edge_start__split_first</bpmn:outgoing>
        </bpmn:startEvent>
        <bpmn:eventBasedGateway id="id_node_split_first" >
            <bpmn:incoming>id_edge_start__split_first</bpmn:incoming>
            <bpmn:outgoing>id_edge_split_first__initial_customer_contact</bpmn:outgoing>
            <bpmn:outgoing>id_edge_split_first__timer</bpmn:outgoing>            
        </bpmn:eventBasedGateway>
        <bpmn:userTask id="id_node_initial_customer_contact" name="Initial Customer Contact">
            <bpmn:incoming>id_edge_split_first__initial_customer_contact</bpmn:incoming>
            <bpmn:outgoing>id_edge_initial_customer_contact__join</bpmn:outgoing>
        </bpmn:userTask>
        <bpmn:intermediateCatchEvent id="id_node_timer" >
            <bpmn:incoming>id_edge_split_first__timer</bpmn:incoming>
            <bpmn:outgoing>id_edge_timer__manager_contact</bpmn:outgoing>
            <bpmn:timerEventDefinition><bpmn:timeDuration>PT120S</bpmn:timeDuration></bpmn:timerEventDefinition>
        </bpmn:intermediateCatchEvent>
        <bpmn:scriptTask id="id_node_manager_contact" name="Manager Contact">
            <bpmn:incoming>id_edge_timer__manager_contact</bpmn:incoming>
            <bpmn:outgoing>id_edge_manager_contact__join</bpmn:outgoing>
        </bpmn:scriptTask>
        <bpmn:parallelGateway id="id_node_join" >
            <bpmn:incoming>id_edge_initial_customer_contact__join</bpmn:incoming>
            <bpmn:incoming>id_edge_manager_contact__join</bpmn:incoming>
            <bpmn:outgoing>id_edge_join__end</bpmn:outgoing>
        </bpmn:parallelGateway>
        <bpmn:endEvent id="id_node_end" >
            <bpmn:incoming>id_edge_join__end</bpmn:incoming>
        </bpmn:endEvent>
        <bpmn:sequenceFlow id="id_edge_start__split_first" sourceRef="id_node_start" targetRef="id_node_split_first" />
        <bpmn:sequenceFlow id="id_edge_split_first__initial_customer_contact" sourceRef="id_node_split_first" targetRef="id_node_initial_customer_contact" />
        <bpmn:sequenceFlow id="id_edge_split_first__timer" sourceRef="id_node_split_first" targetRef="id_node_timer" />
        <bpmn:sequenceFlow id="id_edge_timer__manager_contact" sourceRef="id_node_timer" targetRef="id_node_manager_contact" />
        <bpmn:sequenceFlow id="id_edge_initial_customer_contact__join" sourceRef="id_node_initial_customer_contact" targetRef="id_node_join" />
        <bpmn:sequenceFlow id="id_edge_manager_contact__join" sourceRef="id_node_manager_contact" targetRef="id_node_join" />
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
            <bpmndi:BPMNShape id="id_shape_split_first" bpmnElement="id_node_split_first">
                <dc:Bounds x="75" y="125" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_initial_customer_contact" bpmnElement="id_node_initial_customer_contact">
                <dc:Bounds x="150" y="1" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_timer" bpmnElement="id_node_timer">
                <dc:Bounds x="200" y="225" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_manager_contact" bpmnElement="id_node_manager_contact">
                <dc:Bounds x="325" y="200" width="150" height="100" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_join" bpmnElement="id_node_join">
                <dc:Bounds x="500" y="125" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNShape id="id_shape_end" bpmnElement="id_node_end">
                <dc:Bounds x="575" y="125" width="50" height="50" />
                <bpmndi:BPMNLabel>
                    <dc:Bounds x="296" y="196" width="26" height="12" />
                </bpmndi:BPMNLabel>
            </bpmndi:BPMNShape>
            <bpmndi:BPMNEdge id="id_edge_shape_start__split_first" bpmnElement="id_edge_start__split_first" sourceElement="id_shape_start" targetElement="id_shape_split_first">
                <di:waypoint xsi:type="dc:Point" x="51" y="150" />
                <di:waypoint xsi:type="dc:Point" x="75" y="150" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_split_first__initial_customer_contact" bpmnElement="id_edge_split_first__initial_customer_contact" sourceElement="id_shape_split_first" targetElement="id_shape_initial_customer_contact">
                <di:waypoint xsi:type="dc:Point" x="100" y="125" />
                <di:waypoint xsi:type="dc:Point" x="100" y="51" />
                <di:waypoint xsi:type="dc:Point" x="150" y="51" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_split_first__timer" bpmnElement="id_edge_split_first__timer" sourceElement="id_shape_split_first" targetElement="id_shape_timer">
                <di:waypoint xsi:type="dc:Point" x="100" y="175" />
                <di:waypoint xsi:type="dc:Point" x="100" y="250" />
                <di:waypoint xsi:type="dc:Point" x="200" y="250" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_timer__manager_contact" bpmnElement="id_edge_timer__manager_contact" sourceElement="id_shape_timer" targetElement="id_shape_manager_contact">
                <di:waypoint xsi:type="dc:Point" x="250" y="250" />
                <di:waypoint xsi:type="dc:Point" x="325" y="250" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_initial_customer_contact__join" bpmnElement="id_edge_initial_customer_contact__join" sourceElement="id_shape_initial_customer_contact" targetElement="id_shape_join">
                <di:waypoint xsi:type="dc:Point" x="300" y="51" />
                <di:waypoint xsi:type="dc:Point" x="525" y="51" />                
                <di:waypoint xsi:type="dc:Point" x="525" y="125" />                
            </bpmndi:BPMNEdge>            
            <bpmndi:BPMNEdge id="id_edge_shape_manager_contact__join" bpmnElement="id_edge_manager_contact__join" sourceElement="id_shape_manager_contact" targetElement="id_shape_join">
                <di:waypoint xsi:type="dc:Point" x="475" y="250" />
                <di:waypoint xsi:type="dc:Point" x="525" y="250" />
                <di:waypoint xsi:type="dc:Point" x="525" y="175" />
            </bpmndi:BPMNEdge>
            <bpmndi:BPMNEdge id="id_edge_shape_join__end" bpmnElement="id_edge_join__end" sourceElement="id_shape_join" targetElement="id_shape_end">                
                <di:waypoint xsi:type="dc:Point" x="550" y="150" />                
                <di:waypoint xsi:type="dc:Point" x="575" y="150" />                
            </bpmndi:BPMNEdge>
        </bpmndi:BPMNPlane>
    </bpmndi:BPMNDiagram>
</bpmn:definitions>
"""
