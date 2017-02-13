from django.contrib.auth.models import User
from django.test import TestCase
from viewflow.models import Process


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def testApproved(self):
        self.client.post(
            '/workflow/helloworld/helloworld/start/',
            {'text': 'Hello, world',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/workflow/helloworld/helloworld/1/approve/2/assign/'
        )

        self.client.post(
            '/workflow/helloworld/helloworld/1/approve/2/',
            {'approved': True,
             '_viewflow_activation-started': '2000-01-01'}
        )

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(5, process.task_set.count())

    def testNotApproved(self):
        self.client.post(
            '/workflow/helloworld/helloworld/start/',
            {'text': 'Hello, world',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/workflow/helloworld/helloworld/1/approve/2/assign/'
        )

        self.client.post(
            '/workflow/helloworld/helloworld/1/approve/2/',
            {'approved': False,
             '_viewflow_activation-started': '2000-01-01'}
        )

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(4, process.task_set.count())
