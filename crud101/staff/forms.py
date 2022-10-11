from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from viewflow.forms import AjaxModelSelect

from .models import Department, Employee, DeptManager, DeptEmp, Title, Salary


class UpdateDepartmentForm(forms.ModelForm):
    dept_no = forms.CharField(disabled=True)

    class Meta:
        model = Department
        fields = '__all__'


class UpdateEmployeeForm(forms.ModelForm):
    emp_no = forms.CharField(disabled=True)

    class Meta:
        model = Employee
        fields = '__all__'


class ChangeManagerForm(forms.Form):
    manager = forms.ModelChoiceField(
        queryset=Employee.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).all(),
        label=_('Manager'),
        help_text=_('full name'),
        widget=AjaxModelSelect(lookups=['full_name__icontains']))

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department')
        super(ChangeManagerForm, self).__init__(*args, **kwargs)

    def save(self):
        new_manager = self.cleaned_data['manager']

        DeptManager.objects.filter(
            department=self.department
        ).set(
            department=self.department,
            employee=new_manager
        )


class ChangeDepartmentForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label=_('Change department'))

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        super(ChangeDepartmentForm, self).__init__(*args, **kwargs)

    def save(self):
        new_department = self.cleaned_data['department']

        DeptEmp.objects.filter(
            employee=self.employee
        ).set(
            department=new_department,
            employee=self.employee
        )


class ChangeTitleForm(forms.Form):
    position = forms.CharField(label=_('Position'))

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        super(ChangeTitleForm, self).__init__(*args, **kwargs)

    def save(self):
        new_title = self.cleaned_data['position']

        Title.objects.filter(
            employee=self.employee,
        ).set(
            employee=self.employee,
            title=new_title
        )


class ChangeSalaryForm(forms.Form):
    salary = forms.IntegerField(max_value=1000000, label=_('Salary'))

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        super(ChangeSalaryForm, self).__init__(*args, **kwargs)

    def save(self):
        new_salary = self.cleaned_data['salary']

        Salary.objects.filter(
            employee=self.employee,
        ).set(
            employee=self.employee,
            salary=new_salary,
        )
