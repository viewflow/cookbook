from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from viewflow.fsm.rest import FlowRESTMixin

from .flows import ReviewFlow
from .models import Review, ReviewState


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["pk", "stage", "author", "approver", "text", "comment"]
        extra_kwargs = {
            "stage": {"read_only": True},
        }


class ReviewAuditSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        fields = ["comment"]


class ReviewViewSet(FlowRESTMixin, viewsets.ModelViewSet):
    """viewflow.fsm and django restframework integration."""

    flow_state = ReviewFlow.stage
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object_flow(self, request, obj):
        """Instantiate the flow without default constructor"""
        return ReviewFlow(
            obj, user=request.user, ip_address=request.META.get("REMOTE_ADDR")
        )

    def get_serializer_class(self):
        if self.action in ("approve", "reject"):
            return ReviewAuditSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(stage=ReviewState.NEW)

    @action(methods=["POST"], detail=True, url_path="transition/approve")
    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        flow = self.get_object_flow(request, instance)

        if not flow.approve.has_perm(request.user):
            raise PermissionDenied

        if not flow.approve.can_proceed():
            raise ValidationError(_("Transition is not allowed"))

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        flow.approve()

        return Response(serializer.data)
