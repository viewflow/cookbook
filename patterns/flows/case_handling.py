"""
Description:
    Case Handling is a way to assign tasks in a process so that one person (or
    resource) handles all the tasks in a single case. The person is chosen when
    the case starts or when the first task needs to be assigned.

Examples:
    A loan application case: The same loan officer is responsible for reviewing
    the application, contacting the applicant, and finalizing the decision.

Purpose:
    Case Handling ensures consistency and efficiency by having the same person
    work on all tasks within a case. This approach can be strict, requiring one
    person to do everything, or flexible, where the person in charge can assign
    tasks to others or let them choose which tasks to complete. It helps
    maintain quality and simplifies communication by reducing the number of
    people involved in a single case.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process


class CaseHandlingProcess(Process):
    case_details = jsonstore.CharField(max_length=500)
    approved = jsonstore.BooleanField(default=False)
    packaged = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True

    def __str__(self):
        return f"CaseHandlingProcess: {self.case_details[:50]}"


class CaseHandlingFlow(flow.Flow):
    process_class = CaseHandlingProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=["case_details"]))
        .Annotation(title="Submit Case Details")
        .Permission(auto_create=True)
        .Next(this.approve_case)
    )

    approve_case = (
        flow.View(UpdateProcessView.as_view(fields=["approved"]))
        .Annotation(title="Approve Case")
        .Assign(this.start.owner)
        .Next(this.package_goods)
    )

    package_goods = (
        flow.View(UpdateProcessView.as_view(fields=["packaged"]))
        .Annotation(title="Package Goods")
        .Assign(this.approve_case.owner)
        .Next(this.end)
    )

    end = flow.End()

    process_description = (
        "This process assigns all tasks in a single case to the same user, ensuring consistency and efficiency "
        "throughout the process."
    )

    def __str__(self):
        return "Case Handling Flow"


class TestCaseHandlingFlow(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = User.objects.create_user(
            username="case_handler", password="password"
        )

    def test_flow(self):
        self.client.login(username="case_handler", password="password")

        # Start the process and submit case details
        response = self.client.post(
            CaseHandlingFlow.start.reverse("execute"),
            {"case_details": "Details about the case."},
        )
        self.assertEqual(response.status_code, 302)

        # Approve the case
        process = CaseHandlingProcess.objects.get()
        approval_task = process.task_set.get(flow_task=CaseHandlingFlow.approve_case)
        self.client.post(approval_task.reverse("assign"), {})
        response = self.client.post(
            approval_task.reverse("execute"), {"approved": True}
        )
        self.assertEqual(response.status_code, 302)

        # Package the goods
        packaging_task = process.task_set.get(flow_task=CaseHandlingFlow.package_goods)
        self.client.post(packaging_task.reverse("assign"), {})
        response = self.client.post(
            packaging_task.reverse("execute"), {"packaged": True}
        )
        self.assertEqual(response.status_code, 302)

        # Verify process completion
        process.refresh_from_db()
        self.assertTrue(process.approved)
        self.assertTrue(process.packaged)
