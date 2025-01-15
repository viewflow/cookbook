"""
Description
    This feature allows you to assign specific roles to tasks during the design
    phase. At runtime, these tasks will be distributed to all resources that
    belong to the assigned roles. Roles group resources with similar
    characteristics, making it easier to allocate work effectively.

Example:
    The "Approve Travel Request" task is assigned to Managers.

Motivation
    Role-based Distribution is one of the most common ways to assign work in
    Process-Aware Information Systems (PAIS). It allows the system to send tasks
    to the most suitable resources when the task is ready to be worked on. The
    actual resource is only chosen at runtime, providing flexibility. By
    defining roles in the process model, you can identify resource groups
    responsible for specific tasks. This approach makes processes adaptable
    since the exact resources within a role don’t need to be determined until
    execution.
"""

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.workflow import act, flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process


class TravelApprovalProcess(Process):
    travel_request_details = jsonstore.CharField(max_length=500)
    approved = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True


class RoleBasedFlow(flow.Flow):
    process_class = TravelApprovalProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=["travel_request_details"]))
        .Annotation(title="Submit Travel Request")
        .Permission(auto_create=True)
        .Next(this.approve_request)
    )

    approve_request = (
        flow.View(UpdateProcessView.as_view(fields=["approved"]))
        .Annotation(title="Approve Request")
        .Permission("travel.can_approve_request")
        .Next(this.check_approval)
    )

    check_approval = (
        flow.If(act.process.approved)
        .Annotation(title="Check Approval")
        .Then(this.approved)
        .Else(this.rejected)
    )

    approved = (
        flow.Function(this.approve_action)
        .Annotation(title="Request Approved")
        .Next(this.end)
    )

    rejected = (
        flow.Function(this.reject_action)
        .Annotation(title="Request Rejected")
        .Next(this.end)
    )

    end = flow.End()

    def approve_action(self, activation):
        print(f"Travel request approved: {activation.process.travel_request_details}")

    def reject_action(self, activation):
        print(f"Travel request rejected: {activation.process.travel_request_details}")

    process_description = (
        "This process handles travel request approvals. Employees submit requests, which are reviewed by managers. "
        "Managers can either approve or reject the requests."
    )

    def __str__(self):
        return "Travel Approval Process Flow"


class TestRoleBasedFlow(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a specific permission
        permission = Permission.objects.create(
            codename="can_approve_request", name="Can approve travel request"
        )

        # Create a Manager group with the permission
        manager_group = Group.objects.create(name="Manager")
        manager_group.permissions.add(permission)

        # Create a Manager user and assign to the group
        manager_user = User.objects.create_user(username="manager", password="password")
        manager_user.groups.add(manager_group)

        # Create another user
        User.objects.create_user(username="employee", password="password")

    def test_flow(self):
        self.client.login(username="employee", password="password")

        # Start the process
        response = self.client.post(
            RoleBasedFlow.start.reverse("execute"),
            {"travel_request_details": "Conference trip to Berlin"},
        )
        self.assertEqual(response.status_code, 302)

        # Manager approval
        self.client.login(username="manager", password="password")
        process = TravelApprovalProcess.objects.get()
        approval_task = process.task_set.get(flow_task=RoleBasedFlow.approve_request)

        self.client.post(approval_task.reverse("assign"), {})
        response = self.client.post(approval_task.reverse("execute"), {"approved": "1"})
        self.assertEqual(response.status_code, 302)

        # Verify process completion
        process.refresh_from_db()
        self.assertTrue(process.approved)
