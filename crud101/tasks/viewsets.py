from viewflow.urls import ModelViewset

from . import models, forms


class TaskViewset(ModelViewset):
    model = models.Task
    list_columns = (
        "name",
        "project",
        "category",
        "subcategory",
        "description",
    )


class CategoryViewset(ModelViewset):
    model = models.TaskCategory
    list_columns = ("name",)
    list_search_fields = ("name",)
    list_order_columns = ("name",)


class SubCategoryViewset(ModelViewset):
    model = models.TaskSubcategory
    list_columns = ("name", "category")
    list_search_fields = ("name", "category__name")
    list_filter_fields = ("category",)
    list_order_columns = ("name", "category")

    def get_queryset(self, request):
        return models.TaskSubcategory.objects.select_related("category").all()


class ProjectViewset(ModelViewset):
    model = models.Project
    update_form_class = forms.ProjectForm
    list_columns = ("name", "description")
    list_search_fields = ("name", "description")
    list_order_columns = ("name",)
