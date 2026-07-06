from django.urls import path

from viewflow import viewprop
from viewflow.workflow.flow import FlowViewset

from .views import AddOrderItemView


class OrderFlowViewset(FlowViewset):
    """A ``FlowViewset`` with an extra process-detail action.

    Adds an ``add_item`` URL (``<pk>/add-item/``) reachable from the order's
    ``process_detail.html`` (overridden in this app's templates). Everything
    else -- dashboard, process detail, task pages -- is the stock viewset.
    """

    add_item_view_class = AddOrderItemView

    def get_add_item_view_kwargs(self, **kwargs):
        return self.filter_kwargs(self.add_item_view_class, **kwargs)

    @viewprop
    def add_item_view(self):
        return self.add_item_view_class.as_view(**self.get_add_item_view_kwargs())

    @property
    def add_item_path(self):
        return path("<int:process_pk>/add-item/", self.add_item_view, name="add_item")
