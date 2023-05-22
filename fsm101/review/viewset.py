from django.urls import include, path, reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import redirect
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from viewflow.fsm import FlowViewsMixin
from viewflow.forms import TrixEditorWidget
from viewflow.views import CreateModelView
from viewflow.urls import Application, CreateViewMixin, ReadonlyModelViewset, route

from .flows import ReviewFlow
from .models import Review, ReviewState
from .views import reject_view
from .rest import ReviewViewSet


router = routers.DefaultRouter()
router.register(r"", ReviewViewSet)


class AddReviewView(CreateModelView):
    model = Review
    fields = ["title", "text"]
    form_widgets = {
        "text": TrixEditorWidget,
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.stage = ReviewState.NEW
        self.object.save()
        return redirect(self.get_success_url())


class ReviewViewset(FlowViewsMixin, CreateViewMixin, ReadonlyModelViewset):
    icon = "menu_book"
    model = Review
    flow_state = ReviewFlow.stage
    list_columns = (
        "__str__",
        "author",
        "published",
        "approver",
        "stage",
    )
    list_filter_fields = ("stage",)
    create_view_class = AddReviewView

    def get_object_flow(self, request, obj):
        return ReviewFlow(
            obj, user=request.user, ip_address=request.META.get("REMOTE_ADDR")
        )

    def get_transition_fields(self, request, obj, slug):
        if slug == "approve":
            return ["text", "comment"]
        else:
            return []

    @property
    def remove_path(self):
        return path(
            "<path:pk>/transition/reject/", reject_view, name="transition_remove"
        )


class ReviewApplication(Application):
    title = "FSM Flow Demo"
    icon = "fact_check"
    menu_template_name = "review/app_menu.html"
    permission = (lambda user: user.is_staff,)

    reviews_path = route("review/", ReviewViewset())
    swagger_path = path(
        "api/swagger/",
        TemplateView.as_view(
            template_name="viewflow/contrib/swagger.html",
            extra_context={"api_url": reverse_lazy("review:schema")},
        ),
        name="swagger",
    )
    schema_path = path("api/schema/", get_schema_view(title="FSM 101"), name="schema")
    api_path = path("api/", include(router.urls))
