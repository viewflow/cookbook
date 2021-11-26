from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Review, ReviewState, ReviewChangeLog
from ..flows import ReviewFlow


class Test(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="john")

    def test_flow_approved(self):
        review = Review(author=self.user, text="sample text")
        flow = ReviewFlow(review, self.user, "127.0.0.1")

        flow.approve()
        self.assertTrue(
            review.pk is not None
        )  # saved in ReviewFlow._on_success_transition
        self.assertEqual(review.stage, ReviewState.APPROVED.value)

        flow.publish()
        self.assertEqual(review.stage, ReviewState.PUBLISHED.value)

        flow.remove()
        self.assertEqual(review.stage, ReviewState.REMOVED.value)

        logs = ReviewChangeLog.objects.filter(review=review)
        self.assertEqual(3, logs.count())
