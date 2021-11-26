from django.contrib.auth.models import User
from django.test import TestCase, override_settings, tag
from ..models import Review, ReviewState


@tag("integration")
@override_settings(ROOT_URLCONF=__name__.rsplit(".", 3)[0] + ".config.urls")
class Test(TestCase):  # noqa: D101
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@admin.com", "admin")
        self.assertTrue(self.client.login(username="admin", password="admin"))

    def test_admin_list_page(self):
        response = self.client.get("/admin/review/review/")
        self.assertEqual(response.status_code, 200)

    def test_admin_detail_page(self):
        review = Review.objects.create(
            text="Test", author=self.admin, stage=ReviewState.NEW
        )
        response = self.client.get("/admin/review/review/%d/change/" % review.pk)
        self.assertEqual(response.status_code, 200)

    def test_admin_default_transition_page(self):
        review = Review.objects.create(
            text="Test", author=self.admin, stage=ReviewState.NEW
        )
        response = self.client.get(
            "/admin/review/review/%d/transition/remove/" % review.pk
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_invalid_transition_page(self):
        review = Review.objects.create(
            text="Test", author=self.admin, stage=ReviewState.NEW
        )
        response = self.client.get(
            "/admin/review/review/%d/transition/__invalid__/" % review.pk
        )
        self.assertEqual(response.status_code, 400)

    def test_admin_custom_fields_transition_page(self):
        review = Review.objects.create(
            text="Test", author=self.admin, stage=ReviewState.NEW
        )
        response = self.client.get(
            "/admin/review/review/%d/transition/approve/" % review.pk
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_custom_view_transition_page(self):
        review = Review.objects.create(
            text="Test", author=self.admin, stage=ReviewState.NEW
        )
        response = self.client.get(
            "/admin/review/review/%d/transition/reject/" % review.pk
        )
        self.assertEqual(response.status_code, 200)
