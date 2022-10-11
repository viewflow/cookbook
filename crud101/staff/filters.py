from django.db.models import Exists, OuterRef
from django.utils import timezone
from django_filters import FilterSet, ModelChoiceFilter
from .models import Department, DeptEmp


class EmployeeFilterSet(FilterSet):
    department = ModelChoiceFilter(
        queryset=Department.objects.all(), method="filter_department", label="Department",
    )

    def filter_department(self, queryset, name, value):
        today = timezone.now().date()
        return queryset.filter(
            Exists(
                DeptEmp.objects.filter(
                    department=value,
                    employee=OuterRef("pk"),
                    from_date__lte=today,
                    to_date__gt=today,
                )
            )
        )
