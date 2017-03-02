from django.db.models import Q
from guardian.models import UserObjectPermission
from viewflow.activation import STATUS
from viewflow.models import Task

from .payments.flow import BillFlow


def user_queue(flow_classes, user):
    queryset = Task.filter_available(
        flow_classes,
        user
    ).filter(
        flow_task_type='HUMAN',
        status=STATUS.NEW
    )

    if not user.is_superuser:
        all_object_perms = set(user.get_all_permissions())
        per_object_perms = {
            '{}.{}'.format(userperm.content_type.app_label, userperm.permission.codename)
            for userperm in UserObjectPermission.objects.filter(user=user)
        } - all_object_perms

        has_permission = (
            Q(owner_permission__in=all_object_perms | per_object_perms) |
            Q(owner_permission__isnull=True) |
            Q(owner=user)
        )

        queryset = queryset.filter(
            has_permission
        ).exclude(
            process__flow_class=BillFlow,
            process__order_department__nq=user.department
        )

    return queryset
