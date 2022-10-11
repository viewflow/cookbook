from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, render, redirect
from viewflow.forms import get_ajax_suggestions
from viewflow.views import ListModelView

from .models import Department, Employee, DeptEmp
from .forms import ChangeManagerForm, ChangeSalaryForm, ChangeTitleForm, ChangeDepartmentForm


@permission_required("employees.change_deptmanager")
def change_manager(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = ChangeManagerForm(department=department, data=request.POST or None)

    if request.method == "OPTIONS":
        query = request.META.get('HTTP_X_REQUEST_AUTOCOMPLETE', request.body)
        options = QueryDict(query, encoding=request.encoding)
        field = form.base_fields.get(options.get("field"))
        query = options.get("query")
        if field is None or query is None:
            return JsonResponse({"error": "Field or Query is missing"}, status=400)
        return JsonResponse({"suggestions": get_ajax_suggestions(field, query)})
    elif request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f"{request.resolver_match.namespace}:detail", department.pk)

    return render(request, "staff/manager_change.html", {
        "form": form,
        "department": department,
        "model": Department
    })


@permission_required("employees.change_salary")
def change_salary(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = ChangeSalaryForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(f"{request.resolver_match.namespace}:detail", employee.pk)

    return render(request, 'staff/salary_change.html', {
        'form': form,
        'employee': employee,
    })


@permission_required("employees.change_title")
def change_title(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = ChangeTitleForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(f"{request.resolver_match.namespace}:detail", employee.pk)

    return render(request, 'staff/title_change.html', {
        'form': form,
        'employee': employee,
    })


@permission_required('employees.change_deptemp')
def change_department(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = ChangeDepartmentForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(f"{request.resolver_match.namespace}:detail", employee.pk)

    return render(request, 'staff/employee_department_change.html', {
        'form': form,
        'employee': employee,
    })


class DepartmentEmployeesListView(ListModelView):
    model = Employee
    columns = ('emp_no', 'first_name', 'last_name', 'works_since', 'birth_date')
    template_name = 'staff/department_employees_list.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.department = get_object_or_404(Department, pk=self.kwargs.get('pk', -1))

    def get_queryset(self):
        today = timezone.now().date()
        queryset = super().get_queryset()
        return queryset.filter(
            deptemp__department=self.department,
            deptemp__from_date__lte=today,
            deptemp__to_date__gt=today
        )

    def works_since(self, obj):
        return DeptEmp.objects.filter(employee=obj).current().from_date

    def get_object_url(self, obj):
        return reverse('staff:employee:detail', args=[obj.pk])
