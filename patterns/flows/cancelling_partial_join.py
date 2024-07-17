"""
Description:
    When two or more branches join back into one after splitting, the next task
    begins when a certain number of these branches are completed. If this number
    is reached, the other branches are canceled, and the process restarts.

Example:
    After getting a picture, it is sent to three art dealers for review. When
    two of them finish their tasks, the third task is canceled, and the
    restoration task begins.

Purpose:
    This pattern speeds up the process by continuing when only some tasks are
    done, not all. It synchronizes branches but only needs a specific number to
    finish.
"""

import time
import random

from celery import shared_task
from viewflow import this, jsonstore
from viewflow.contrib import celery
from viewflow.workflow import flow
from viewflow.workflow.flow import views
from viewflow.workflow.models import Process


class ReviewProcess(Process):
    image = jsonstore.URLField()
    quote1 = jsonstore.DecimalField(default=0)
    quote2 = jsonstore.DecimalField(default=0)
    quote3 = jsonstore.DecimalField(default=0)

    class Meta:
        proxy = True


class CancelingPartialJoin(flow.Flow):
    process_class = ReviewProcess

    start = (
        flow.Start(views.CreateProcessView.as_view(fields=["image"]))
        .Annotation(title="Upload Picture")
        .Next(this.split)
    )

    split = (
        flow.Split()
        .Next(this.get_quote_1)
        .Next(this.get_quote_2)
        .Next(this.get_quote_3)
    )

    get_quote_1 = celery.Job(this.get_quoute_1_task).Next(this.join)

    get_quote_2 = celery.Job(this.get_quoute_2_task).Next(this.join)

    get_quote_3 = celery.Job(this.get_quoute_3_task).Next(this.join)

    join = flow.Join(continue_on_condition=this.required_quotes_received).Next(
        this.restoration
    )

    restoration = flow.Function(this.perform_restoration).Next(this.end)

    end = flow.End()

    def required_quotes_received(self, activation, active_tasks):
        process = activation.process
        quotes = [process.quote1, process.quote2, process.quote3]
        non_zero_quotes = [quote for quote in quotes if quote != 0]
        return len(non_zero_quotes) >= 2

    @staticmethod
    @shared_task
    def get_quoute_1_task(activation_ref):
        time.sleep(random.randint(1, 10))

        with celery.Job.activate(activation_ref) as activation:
            with activation.flow_class.lock(activation.process.pk):
                activation.process.quote1 = random.randint(10, 50)
                activation.process.save(update_fields=["data"])

    @staticmethod
    @shared_task
    def get_quoute_2_task(activation_ref):
        time.sleep(random.randint(1, 10))

        with celery.Job.activate(activation_ref) as activation:
            with activation.flow_class.lock(activation.process.pk):
                activation.process.quote2 = random.randint(10, 50)
                activation.process.save(update_fields=["data"])

    @staticmethod
    @shared_task
    def get_quoute_3_task(activation_ref):
        time.sleep(random.randint(1, 10))

        with celery.Job.activate(activation_ref) as activation:
            with activation.flow_class.lock(activation.process.pk):
                activation.process.quote3 = random.randint(10, 50)
                activation.process.save(update_fields=["data"])

    def perform_restoration(self, activation):
        value = min(
            activation.process.quote1 or 0,
            activation.process.quote2 or 0,
            activation.process.quote3 or 0,
        )
        print(f"Min restoration quote {value}")

    process_description = (
        "After getting a picture, it is sent to three art dealers for review. When "
        "two of them finish their tasks, the third task is canceled, and the "
        "restoration task begins."
    )

    def __str__(self) -> str:
        return (
            "This pattern speeds up the process by continuing when only some tasks are "
            "done, not all. It synchronizes branches but only needs a specific number to "
            "finish."
        )
