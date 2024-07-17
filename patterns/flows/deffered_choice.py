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

from viewflow import this, jsonstore
from viewflow.contrib import celery
from viewflow.workflow import flow
from viewflow.workflow.models import Process
from viewflow.workflow.flow import views


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
