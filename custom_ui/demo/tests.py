from django.contrib.auth.models import User
from django.test import TestCase
from viewflow.models import Process


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def testApproved(self):
        self.client.post(
            '/parcel/delivery/start/',
            {'planet': 'Mars',
             'description': 'Three quarks for Muster Mark!',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/parcel/delivery/1/approve/2/',
            {'approved': True,
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/parcel/delivery/1/delivery/4/assign/',
        )

        self.client.post(
            '/parcel/delivery/1/delivery/4/',
            {'drop_status': 'SCF',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/parcel/delivery/1/report/5/',
            {'delivery_report': 'Unobservable',
             '_viewflow_activation-started': '2000-01-01'}
        )

        process = Process.objects.get()
        self.assertEquals('DONE', process.status)
        self.assertEquals(6, process.task_set.count())

    def testNotApproved(self):
        self.client.post(
            '/parcel/delivery/start/',
            {'planet': 'Mars',
             'description': 'Three quarks for Muster Mark!',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/parcel/delivery/1/approve/2/',
            {'approved': False,
             '_viewflow_activation-started': '2000-01-01'}
        )

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(4, process.task_set.count())
