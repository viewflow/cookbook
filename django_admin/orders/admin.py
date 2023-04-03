from django.contrib import admin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import models
from django.forms import TextInput, Textarea
from .models import Order, OrderItem, Customer


class CachedPaginator(Paginator):
    CACHE_KEY_PREFIX = "paginator"

    @property
    def count(self):
        key = f"{self.CACHE_KEY_PREFIX}:{hash(self.object_list.query)}"
        count = cache.get(key)
        if count is None:
            count = super().count
            cache.set(key, count, 3600)  # Cache for 1 hour
        return count


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ["make_published"]
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = False
    date_hierarchy = "created"
    empty_value_display = "-empty-"
    exclude = ["modified"]
    # fields = ["customer", "description"]
    fieldsets = (
        (None, {"fields": ("customer", "description")}),
        (
            "Advanced options",
            {"classes": ("collapse",), "fields": ("status", "tags", "options")},
        ),
    )
    filter_horizontal = ["tags"]
    filter_vertical = ["options"]
    # form
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "40"})},
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
        models.DecimalField: {"widget": TextInput(attrs={"size": "10"})},
    }
    inlines = [OrderItemInline]
    list_display = [
        "pk",
        "customer",
        "description",
        "total",
        "status",
        "created",
        "modified",
    ]
    list_display_links = ["pk", "customer"]
    list_editable = ["status"]
    list_filter = ["status", "created", "modified", "tags", "options"]
    list_max_show_all = 500
    list_per_page = 200
    list_select_related = ("customer",)
    ordering = ("created",)
    paginator = CachedPaginator
    # prepopulated_fields = {"slug": ("customer", "description")}
    preserve_filters = True
    radio_fields = {"status": admin.VERTICAL}
    autocomplete_fields = ["customer"]
    raw_id_fields = ["customer"]
    readonly_fields = ["created", "modified"]
    save_as = True
    save_as_continue = True
    save_on_top = True
    search_fields = ["description", "customer__name", "customer__email"]
    search_help_text = "Order description or customer name or email"
    show_full_result_count = False
    sortable_by = ["status"]
    view_on_site = False

    @admin.action(description="Mark selected stories as published")
    def make_published(self, request, queryset):
        queryset.update(status="p")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
    )
    search_fields = ("name", "email")
