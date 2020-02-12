from viewflow.models import Task
from .flows import DeliveryFlow


def tasks_counts(request):
    if request.user.is_authenticated:
        return {
            'inbox_count': Task.objects.inbox([DeliveryFlow], request.user).count(),
            'queue_count': Task.objects.queue([DeliveryFlow], request.user).count()
        }
    return {}
