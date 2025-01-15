"""
Description:
    The ability to specify at design time the identity of the resource(s) to
    which instances of this task will be distributed at runtime.

Example:
    The Fix Bentley task must only be undertaken by Fred

Purpose:
    Direct Distribution offers the ability for a process designer to precisely
    specify the identity of the resource to which instances of a task will be
    distributed at runtime. This is particularly useful where it is known that a
    task can only be effectively undertaken by a specific resource as it
    prevents the problem of unexpected or non-suitable resource distributions
    arising at runtime by ensuring work items are routed to specific resources,
    a feature that is particularly desirable for critical tasks.
"""

from django.contrib.auth.models import User
from viewflow import this, jsonstore
from viewflow.workflow import flow
from viewflow.workflow.models import Process
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView


class DirectTaskProcess(Process):
    car_model = jsonstore.CharField(max_length=250)
    repair_description = jsonstore.CharField(max_length=1000, blank=True)
    work_done = jsonstore.CharField(max_length=1000, blank=True)

    class Meta:
        proxy = True


def assign_repair_task(activation):
    """Assign task based on car model."""
    if activation.process.car_model.lower() == "bentley":
        return User.objects.filter(username="fred").first()
    return None


class DirectDistributionFlow(flow.Flow):
    process_class = DirectTaskProcess

    start = (
        flow.Start(
            CreateProcessView.as_view(fields=["car_model", "repair_description"])
        )
        .Annotation(title="Start Repair Process")
        .Permission(auto_create=True)
        .Next(this.record_work)
    )

    record_work = (
        flow.View(UpdateProcessView.as_view(fields=["work_done"]))
        .Assign(assign_repair_task)  # Use the custom assignment function
        .Annotation(title="Repair Task")
        .Next(this.end)
    )

    end = flow.End()

    process_description = "Assign repair task based on car model. For Bentley cars, the task is assigned to Fred."

    def __str__(self) -> str:
        return (
            "Tasks are distributed directly based on car type. If the car is a Bentley, "
            "Fred is assigned to handle the task. Other cars remain unassigned."
        )
