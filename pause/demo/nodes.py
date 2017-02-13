from django.core.urlresolvers import reverse

from viewflow.activation import Activation, STATUS
from viewflow.flow import View
from viewflow.flow.activation import ManagedViewActivation


class PausableViewActivation(ManagedViewActivation):
    @Activation.status.transition(
        source=[STATUS.ASSIGNED, 'PAUSED'],
        target=STATUS.PREPARED)
    def prepare(self, *args, **kwargs):
        super(PausableViewActivation, self).prepare.original(*args, **kwargs)

    @Activation.status.transition(source=STATUS.PREPARED, target='PAUSED')
    def pause(self):
        self.task.save()


class PausableView(View):
    activation_cls = PausableViewActivation

    def get_task_url(self, task, url_type='guess', namespace='', **kwargs):
        user = kwargs.get('user', None)

        if task.status == 'PAUSED':
            if url_type in ['guess', 'execute'] and self.can_execute(user, task):
                return reverse(
                    '{}:{}'.format(namespace, self.name),
                    kwargs={
                        'process_pk': task.process_id,
                        'task_pk': task.pk
                    })

        return super(PausableView, self).get_task_url(
            task, url_type=url_type, namespace=namespace, **kwargs)
