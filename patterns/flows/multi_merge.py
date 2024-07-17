"""
Description: 
    Two or more branches come together into one branch. When any of the incoming
    branches is active, the control moves to the next branch.

Example:
    The tasks lay_foundations, order_materials, and book_labourer run at the
    same time. After each task is finished, the quality_review task runs before
    completing that part of the process.

Purpose:
    The Multi-Merge pattern lets different branches of a process join into one
    branch. Even though multiple paths are combined, there is no waiting for
    synchronization, and each active branch continues into the merged branch
    without delay.
"""

from viewflow import this, jsonstore
from viewflow.workflow import flow
from viewflow.workflow.flow import views
from viewflow.workflow.models import Process


class ConstructionProcess(Process):
    description = jsonstore.CharField()

    foundations_laid = jsonstore.BooleanField(default=False)
    materials_ordered = jsonstore.BooleanField(default=False)
    labourer_booked = jsonstore.BooleanField(default=False)

    verified_tasks = jsonstore.JSONField(default=list)

    class Meta:
        proxy = True


class MultiMerge(flow.Flow):
    process_description = """
    The tasks lay_foundations, order_materials, and book_labourer run at the
    same time. After each task is finished, the quality_review task runs before
    completing that part of the process.
    """

    process_class = ConstructionProcess

    start = flow.Start(
        views.CreateProcessView.as_view(fields=["description"]),
    ).Next(this.split)

    split = (
        flow.Split()
        .Next(this.lay_foundations)
        .Next(this.order_materials)
        .Next(this.book_labourer)
    )

    lay_foundations = flow.View(
        views.UpdateProcessView.as_view(
            fields=["foundations_laid"],
        )
    ).Next(this.quality_review, task_data=lambda _: {"action": "lay_foundations"})

    order_materials = flow.View(
        views.UpdateProcessView.as_view(
            fields=["materials_ordered"],
        )
    ).Next(this.quality_review, task_data=lambda _: {"action": "order_materials"})

    book_labourer = flow.View(
        views.UpdateProcessView.as_view(
            fields=["labourer_booked"],
        )
    ).Next(this.quality_review, task_data=lambda _: {"action": "book_labourer"})

    quality_review = (
        flow.Function(this.perform_quality_review)
        .Annotation(
            title="Quality review (3 times)",
        )
        .Next(this.join)
    )

    join = flow.Join().Next(this.end)

    end = flow.End()

    def perform_quality_review(self, activation):
        activation.process.verified_tasks = activation.process.verified_tasks + [
            activation.task.data["action"]
        ]
        activation.process.save(update_fields=["data"])

    def __str__(self) -> str:
        return (
            "Two or more branches come together into one branch. When any of the incoming"
            "branches is active, the control moves to the next branch."
        )
