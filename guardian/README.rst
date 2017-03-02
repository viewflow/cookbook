============================
Object-level permission demo
============================

This process demonstrates viewflow and django-guardian integration.


Quick start
===========

** TBD ***


Description
===========

This is the sample for the bill acceptance and payment workflow.

Object-level permission used to restrict bill processing depends on a user department.

The `fixtures/demo_data.json` contans users and permission sample, where each head manager can accept
bills coming for the own department only::


    accept_bill = flow.View(
        UpdateProcessView,
        fields=[
            'accepted'
        ]
    ).Permission(
        'department.can_accept_bill',
        obj=lambda process: process.department
    ).Next(this.check_bill_accept)

