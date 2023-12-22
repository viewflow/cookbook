from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow import views
from . import tasks


class ReassignFlow(flow.Flow):
    start = flow.Start(views.CreateProcessView.as_view(fields=[])).Next(this.task)
    task = (
        flow.View(views.UpdateProcessView.as_view(fields=[]))
        .Assign(this.start.owner)
        .onCreate(this.unassign_on_timeout)
        .Next(this.end)
    )
    end = flow.End()

    def unassign_on_timeout(self, activation):
        tasks.unassign_task.apply_async(
            [activation.task.pk], countdown=60
        )  # 1 minute to complete
