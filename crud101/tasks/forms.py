from django import forms
from django.forms.models import inlineformset_factory
from viewflow.forms import (
    DependentModelSelect,
    InlineFormSetField,
    ModelForm,
    Layout,
    Row,
    Column,
)
from .models import Project, Task, TaskCategory, TaskSubcategory


class TaskForm(ModelForm):
    subcategory = forms.ModelChoiceField(
        queryset=TaskSubcategory.objects.all(),
        widget=DependentModelSelect(
            depends_on="category",
            queryset=lambda category: TaskSubcategory.objects.filter(category=category),
        ),
    )

    Layout = Layout(
        Column("name", "description"),
        Column("category", "subcategory"),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "category", "subcategory"]


TaskInlineFormset = inlineformset_factory(
    Project,
    Task,
    fields=["name", "description", "category", "subcategory"],
    extra=2,
    can_delete=False,
    form=TaskForm,
)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]

    tasks = InlineFormSetField(Project, Task, formset_class=TaskInlineFormset)
