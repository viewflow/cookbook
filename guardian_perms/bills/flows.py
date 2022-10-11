from viewflow import this
from viewflow.workflow import flow, act
from viewflow.workflow.flow.views import CreateArtifactView, UpdateProcessView, UpdateArtifactView

from .models import BillProcess, Bill


class BillClearingFlow(flow.Flow):
    process_class = BillProcess

    # office
    register_bill = (
        flow.Start(
            CreateArtifactView.as_view(
                model=Bill,
                fields=["order_department", "order_item", "quantity", "description"]
            )
        )
        .Permission("department.can_register_bill")
        .Next(this.accept_bill)
    )

    # project manager
    accept_bill = (
        flow.View(UpdateProcessView.as_view(fields=["accepted"]))
        .Permission(
            "department.can_accept_bill",
            obj=lambda process: process.artifact.order_department,
        )
        .Next(this.check_bill_accept)
    )

    check_bill_accept = (
        flow.If(act.process.accepted)
        .Then(this.sign_bill)
        .Else(this.incorrect_bill)
    )

    incorrect_bill = flow.End()

    # board member
    sign_bill = (
        flow.View(UpdateProcessView.as_view(fields=["signed"]))
        .Permission(
            "department.can_sign_bill",
            obj=lambda process: process.artifact.order_department,
        )
        .Next(this.check_bill_sign)
    )

    check_bill_sign = (
        flow.If(act.process.signed)
        .Then(this.validate_bill)
        .Else(this.bill_rejected)
    )

    bill_rejected = flow.End()

    # bookkeeping
    validate_bill = (
        flow.View(UpdateProcessView.as_view(fields=["validated"]))
        .Permission(
            "department.can_validate_bill",
            obj=lambda process: process.artifact.order_department,
        )
        .Next(this.check_bill_valid)
    )

    check_bill_valid = (
        flow.If(act.process.validated)
        .Then(this.set_bill_paydate)
        .Else(this.accept_bill)
    )

    pay_bill = (
        flow.View(UpdateProcessView.as_view(fields=[]))
        .Permission(
            "department.can_pay_bill",
            obj=lambda process: process.artifact.order_department,
        )
        .Next(this.bill_paid)
    )

    bill_paid = flow.End()

    # financial department
    set_bill_paydate = (
        flow.View(UpdateArtifactView.as_view(fields=["payment_date"]))
        .Permission(
            "department.can_set_bill_paydate",
            obj=lambda process: process.artifact.order_department,
        )
        .Next(this.pay_bill)
    )
