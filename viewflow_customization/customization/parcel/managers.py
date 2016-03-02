from django.db.models import Manager, Q
from guardian.shortcuts import get_objects_for_user
from viewflow.compat import manager_from_queryset
from viewflow.managers import TaskQuerySet as BaseTaskQuerySet


class TaskQuerySet(BaseTaskQuerySet):
    def user_queue(self, user, flow_cls=None):
        """
        List of tasks permitted for user
        """
        queryset = self.filter(flow_task_type='HUMAN')

        if flow_cls is not None:
            queryset = queryset.filter(process__flow_cls=flow_cls)

        user_planets = get_objects_for_user(user, 'parcel.land_on_planet')
        has_permission = Q(owner__isnull=True, process__parcel__planet__in=user_planets) \
            | Q(owner=user)

        queryset = queryset.filter(has_permission)

        return queryset

TaskManager = manager_from_queryset(Manager, TaskQuerySet)
