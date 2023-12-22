from celery import shared_task
from viewflow.workflow.models import Task
from viewflow.workflow.status import STATUS


@shared_task
def unassign_task(task_pk):
    task = Task.objects.get(pk=task_pk)
    with task.activation() as activation:
        if task.status == STATUS.ASSIGNED:
            # or call activation.reassign(user=) to assign to a new person
            activation.unassign()
