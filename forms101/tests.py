from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ROOT_URLCONF=__name__[:-5] + 'config.urls')
class Test(TestCase):  # noqa: D101
    def test_checkout_form(self):
        form_url = reverse('forms:checkout_form')
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(form_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@doe.com',
            'phone': '3727992222',
            'country': '67',
            'city': 'Tallinn',
            'post_code': '15169',
            'address': 'Ravel 5',
            'additional_info': 'Estonian Informatics Center',
            'card_type': 'V',
            'card_holder': 'JOHN DOE',
            'card_number': '4111111111111111',
            'card_ccv2': '000',
            'card_exp_month': '1',
            'card_exp_year': '2024'
        })
        self.assertEqual(response.status_code, 302)

    def test_contact_form(self):
        form_url = reverse('forms:contact_form')
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(form_url, {
            'name': 'John Doe',
            'email': 'john@doe.com',
            'subject': "What's up!",
            'message': "Hey!",
            'send_copy': 1,
        })
        self.assertEqual(response.status_code, 302)

    def test_login_form(self):
        form_url = reverse('forms:login_form')
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(form_url, {
            'email': 'test@test.com',
            'password': 'test123456',
        })
        self.assertEqual(response.status_code, 302)

    def test_profile_form(self):
        form_url = reverse('forms:profile_form')
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(form_url, {
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': ' Doe',
            'form-address-line_1': '7945 Durham St.',
            'form-address-line_2': '--',
            'form-address-state': 'FL',
            'form-address-city': 'Saint Augustine',
            'form-address-zipcode': '32084',
        })
        self.assertEqual(response.status_code, 302)
