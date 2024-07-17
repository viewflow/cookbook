"""
Description:
     Two or more branches join back together after splitting. The next task
     starts when a set number (n) of branches out of the total (m) are done.
     Extra completions do not start the next task. The join resets when all
     branches finish. This connects to a single Parallel Split earlier.

Example:
     When two out of three Expenditure Approval tasks are done, start the Issue
     Cheque task. Wait for the remaining task to finish before starting Issue
     Cheque again.

Purpose: 
    The Structured Partial Join pattern merges multiple branches into one. It
    starts the next task when a certain number of branches are done, without
    waiting for all. This helps move the process forward faster.
"""

from django import forms
from django.shortcuts import render, redirect
from viewflow import this, jsonstore
from viewflow.workflow import flow
from viewflow.workflow.flow import views
from viewflow.workflow.models import Process


class ExpenditureApprovalProcess(Process):
    description = jsonstore.TextField(help_text="Expenditure goal and terms")
    approved_by = jsonstore.JSONField(default=list)

    class Meta:
        proxy = True


class ApprovementForm(forms.Form):
    approved = forms.BooleanField(
        widget=forms.RadioSelect(
            choices=(
                (1, "Yes"),
                (0, "No"),
            ),
            attrs={"inline": True},
        ),
        required=True,
        initial=0,
    )


def approve_view(request, **kwargs):
    form = ApprovementForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data["approved"]:
            request.activation.process.approved_by = [
                request.user.username
            ] + request.activation.process.approved_by
            request.activation.process.save(update_fields=["data"])

        # View is workflow independed and can be used in different flows.
        request.activation.execute()

        # Redirect to the next avaialbe task
        return redirect(request.activation.get_success_url(request))

    return render(request, "viewflow/workflow/task.html", {"form": form})


class PartialJoin(flow.Flow):
    process_class = ExpenditureApprovalProcess

    start = (
        flow.Start(views.CreateProcessView.as_view(fields=["description"]))
        .Annotation(title="New expenditure request")
        .Next(this.split_approval)
    )

    split_approval = (
        flow.Split().Next(this.approve_1).Next(this.approve_2).Next(this.approve_3)
    )

    approve_1 = flow.View(approve_view).Next(this.check_approval)

    approve_2 = flow.View(approve_view).Next(this.check_approval)

    approve_3 = flow.View(approve_view).Next(this.check_approval)

    check_approval = flow.Join(
        continue_on_condition=this.check_approved, cancel_active=False
    ).Next(this.issue_cheque)

    issue_cheque = flow.Function(this.issue_cheque_task).Next(this.end)

    end = flow.End()

    def check_approved(self, activation, _):
        approved_count = len(activation.process.approved_by)
        return approved_count >= 2

    def issue_cheque_task(self, activation):
        print(f"Issuing cheque for: {activation.process.description}")

    process_description = (
        "When two out of three Expenditure Approval tasks are done, start the Issue"
        " Cheque task."
    )

    def __str__(self) -> str:
        return (
            "Two or more branches join back together after splitting. The next task "
            "starts when a set number (n) of branches out of the total (m) are done. "
            "Extra completions do not start the next task. The join resets when all "
            "branches finish. This connects to a single Parallel Split earlier. "
        )
