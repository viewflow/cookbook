from django.urls import path
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from viewflow.workflow.flow import FlowViewset
from viewflow.workflow.models import Process

from .flows import HelloWorldFlow


@override_settings(
    ROOT_URLCONF=__name__,
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True
)
class Test(TestCase):   # noqa: D101
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.assertTrue(self.client.login(username='admin', password='password'))

    def testApproved(self):
        self.assertRedirects(self.client.post(
            '/workflow/start/', {
                'text': 'Hello, world',
                '_viewflow_activation-started': '2000-01-01'
            }
        ), '/workflow/1/start/1/detail/')

        self.assertRedirects(self.client.post(
            '/workflow/1/approve/2/assign/'
        ), '/workflow/1/approve/2/detail/')

        self.assertRedirects(self.client.post(
            '/workflow/1/approve/2/execute/', {
                'approved': True,
                '_viewflow_activation-started': '2000-01-01'
            }
        ), '/workflow/1/approve/2/detail/')

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(5, process.task_set.count())

    def testNotApproved(self):
        self.assertRedirects(self.client.post(
            '/workflow/start/', {
                'text': 'Hello, world',
                '_viewflow_activation-started': '2000-01-01'
            }
        ), '/workflow/1/start/1/detail/')

        self.assertRedirects(self.client.post(
            '/workflow/1/approve/2/assign/'
        ), '/workflow/1/approve/2/detail/')

        self.assertRedirects(self.client.post(
            '/workflow/1/approve/2/execute/', {
                'approved': False,
                '_viewflow_activation-started': '2000-01-01'
            }
        ), '/workflow/1/approve/2/detail/')

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(4, process.task_set.count())


urlpatterns = [
    path('workflow/', FlowViewset(HelloWorldFlow).urls)
]
