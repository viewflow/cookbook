from django.db.models import Value as V
from django.db.models.functions import Concat
from django.urls import path
from django.utils import timezone
from viewflow import Icon
from viewflow.contrib.import_export import ExportViewsetMixin
from viewflow.forms import Layout, Row, Column
from viewflow.urls import DetailViewMixin, ModelViewset
from . import filters, forms, models, views


class DepartmentViewset(DetailViewMixin, ModelViewset):
    icon = Icon('group_work')
    model = models.Department
    list_columns = ("dept_no", "dept_name", "manager", "employees")
    update_form_class = forms.UpdateDepartmentForm

    urlpatterns = [
        path(
            '<path:pk>/change_manager/',
            views.change_manager,
            name="change_manager"
        ),
        path(
            '<path:pk>/employees/',
            views.DepartmentEmployeesListView.as_view(),
            name="employees"
        )
    ]

    def manager(self, obj):
        today = timezone.now().date()
        manager = obj.deptmanager_set.filter(
            from_date__lte=today, to_date__gt=today
        ).first()
        return manager.employee if manager is not None else ""

    def employees(self, obj):
        return obj.deptemp_set.count()


class EmployeeViewset(ExportViewsetMixin, DetailViewMixin, ModelViewset):
    icon = Icon('engineering')
    model = models.Employee
    queryset = models.Employee.objects.annotate(
        full_name=Concat('first_name', V(' '), 'last_name')
    )
    update_form_class = forms.UpdateEmployeeForm
    list_columns = ("emp_no", "first_name", "last_name", "birth_date", "current_salary")
    list_filterset_class = filters.EmployeeFilterSet
    list_search_fields = ("full_name", )
    form_layout = Layout(
        Row(
            Column(
                "emp_no",
                "first_name",
                "last_name",
                desktop=9
            ),
            Column(
                "hire_date",
                "birth_date",
                "gender",
            )
        )
    )

    urlpatterns = [
        path(
            '<path:pk>/change_salary/',
            views.change_salary,
            name="change_salary"
        ),
        path(
            '<path:pk>/change_title/',
            views.change_title,
            name="change_title"
        ),
        path(
            '<path:pk>/change_department/',
            views.change_department,
            name="change_department"
        ),
    ]

    def current_salary(self, obj):
        salary = obj.salary_set.current()
        return salary.salary if salary is not None else 0
