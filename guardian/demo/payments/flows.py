from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from .models import BillProcess


@frontend.register
class BillFlow(Flow):
    process_class = BillProcess

    # office
    register_bill = flow.Start(
        CreateProcessView,
        fields=[
            'order_department',
            'order_item',
            'quantity',
            'description'
        ]
    ).Permission(
        auto_create=True
    ).Next(this.accept_bill)

    # project manager
    accept_bill = flow.View(
        UpdateProcessView,
        fields=[
            'accepted'
        ]
    ).Permission(
        'users.can_accept_bill',
        obj=lambda process: process.billprocess.order_department
    ).Next(this.check_bill_accept)

    check_bill_accept = flow.If(
        lambda act: act.process.accepted
    ).Then(this.sign_bill).Else(this.incorrect_bill)

    incorrect_bill = flow.End()

    # board member
    sign_bill = flow.View(
        UpdateProcessView,
        fields=[
            'signed'
        ]
    ).Permission(
        'users.can_sign_bill',
        obj=lambda process: process.billprocess.order_department
    ).Next(this.check_bill_sign)

    check_bill_sign = flow.If(
        lambda act: act.process.signed
    ).Then(this.validate_bill).Else(this.bill_rejected)

    bill_rejected = flow.End()

    # bookkeeping
    validate_bill = flow.View(
        UpdateProcessView,
        fields=[
            'validated'
        ]
    ).Permission(
        'users.can_validate_bill',
        obj=lambda process: process.billprocess.order_department
    ).Next(this.check_bill_valid)

    check_bill_valid = flow.If(
        lambda act: act.process.validated
    ).Then(this.set_bill_paydate).Else(this.accept_bill)

    pay_bill = flow.View(
        UpdateProcessView
    ).Permission(
        'users.can_pay_bill',
        obj=lambda process: process.billprocess.order_department
    ).Next(this.bill_paid)

    bill_paid = flow.End()

    # financial department
    set_bill_paydate = flow.View(
        UpdateProcessView,
        fields=[
            'payment_date'
        ]
    ).Permission(
        'users.can_set_bill_paydate',
        obj=lambda process: process.billprocess.order_department
    ).Next(this.pay_bill)
