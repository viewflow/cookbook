from viewflow import this
from viewflow.urls import ModelViewset, DeleteViewMixin
from .models import Order


class OrderViewset(DeleteViewMixin, ModelViewset):
    icon = "location_city"
    model = Order

    # TODO Implement easy way to add bulk actions
    # bulk_actions = [
    #     this.make_published
    # ]

    # def make_published(self, request, queryset):
    #     queryset.update(status="p")

    # TODO? Custom Filter for django-filter?
    # date_hierarchy = "created"

    # TODO empty_value_display = "-empty-"

    # TODO exclude = ["modified"]

    ### form_class = forms.OrderForm()
    ### form_layout =

    # TODO custom widget for filter_horizontal = ["tags"] and filter_vertical = ["options"]

    list_columns = [
        "pk",
        "customer",
        "description",
        "total",
        "status",
        "created",
        "modified",
    ]

    list_object_link_columns = ["pk", "customer"]

    # TODO list_editable = ["status"]

    list_filter_fields = ["status", "created", "modified", "tags", "options"]

    # TODO list_max_show_all = 500
    paginate_by = 200  # list_per_page = 200

    # TODO ordering = ("created",)
    # TODO paginator = CachedPaginator

    # TODO? preserve_filters = True
    # TODO radio_fields = {"status": admin.VERTICAL}

    # Part of the form autocomplete_fields = ["customer"]
    # TODO custom widget? raw_id_fields = ["customer"]

    # TODO part of the form readonly_fields = ["created", "modified"]

    # TODO save_as = True
    # TODO save_as_continue = True
    # NOPE save_on_top = True
    list_search_fields = ["description", "customer__name", "customer__email"]

    # TODO search_help_text = "Order description or customer name or email"
    # TODO show_full_result_count = False
    # TODO sortable_by = ["status"]
