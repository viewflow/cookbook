import difflib
from django.db import transaction
from django.utils import timezone
from viewflow import fsm, this
from .models import Review, ReviewState, ReviewChangeLog


class ReviewFlow(object):
    """Review process definition."""

    stage = fsm.State(
        ReviewState,
        default=ReviewState.NEW
    )

    def __init__(self, review: Review, user, ip_address=None):
        self.review = review
        self.initial_text = self.review.text
        self.user = user
        self.ip_address = ip_address

    @stage.setter()
    def _set_review_stage(self, state_value):
        self.review.stage = state_value.value

    @stage.getter()
    def _get_review_stage(self):
        if self.review.stage:
            return ReviewState(self.review.stage)

    @stage.on_success()
    def _on_success_transition(self, descriptor, source, target):
        with transaction.atomic():
            self.review.save()
            ReviewChangeLog.objects.create(
                review=self.review,
                source=source.value,
                target=target.value,
                author=self.user,
                ip_address=self.ip_address,
                diff='\n'.join(
                    difflib.unified_diff([self.initial_text], [self.review.text])
                ) if self.initial_text != self.review.text else ''
            )
            self.initial_text = self.review.text

    @stage.transition(
        source=ReviewState.NEW,
        target=ReviewState.APPROVED,
        permission=this.is_approver
    )
    def approve(self):
        self.review.approver = self.user

    @stage.transition(
        source=ReviewState.NEW,
        target=ReviewState.REJECTED,
        permission=this.is_approver
    )
    def reject(self):
        self.review.approver = self.user

    @stage.transition(
        source=ReviewState.APPROVED,
        target=ReviewState.PUBLISHED
    )
    def publish(self):
        self.review.published = timezone.now()

    @stage.transition(
        source=fsm.State.ANY,
        target=ReviewState.REMOVED
    )
    def remove(self):
        pass

    def is_approver(self, user):
        return user.is_staff
