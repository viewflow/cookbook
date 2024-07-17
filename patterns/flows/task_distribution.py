from typing import Any
from viewflow import this
from viewflow.workflow import flow


class TaskDistribution(flow.Flow):
    """
    Select worker ably to perform a task
    """

    # flow.Start().Permission()

    # Direct user selection
    # flow.View().Assign()

    # Role-based selection if perfroming by assing permission to a user group
    # flow.View().Permission()

    # Deffered distribution
    # flow.View(select_worker).Next(this.deffered_distribution_task, seed=act.task.artifact)

    # flow.View().Assign(act.task.seed)

    # The ability to allocate the work items within a given case to the same resource at the time that the case is commenced
    # flow.View.Assign(this.xxxx.create_by)

    # Custom callable
    # Instances of the Airframe Examination task should be allocated to an Engineer with an aeronautics degree, an Airbus in-service accreditation and more than 10 years experience in Airbus servicing.

    def has_manage_permission(self, user: Any, obj: Any | None = None) -> bool:
        return super().has_manage_permission(user, obj)

    def has_view_permission(self, user: Any, obj: Any | None = None) -> bool:
        return super().has_view_permission(user, obj)
