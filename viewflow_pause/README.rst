=================
Pause task sample
=================

This sample demonstrates how to implement `pause` and save intermediate results
for a view task

.. image:: .flow.png
   :width: 400px



Custom activation
=================

To customize task execution scenarion, we need to implement custom
task activation class.

Task activation class is the simple state machine with single `status`
field. You can override or add new transitions to the class.

In this sample, we add new transition from `PPERARED` state to `PAUSED`, and
overide `prepare` transition to allow to resume work on a task::

    from viewflow.activation import Activation, STATUS
    from viewflow.flow.activation import ManagedViewActivation


    class PausableViewActivation(ManagedViewActivation):
        @Activation.status.transition(
            source=[STATUS.NEW, 'PAUSED'],
            target=STATUS.PREPARED)
        def prepare(self):
            super(PausableViewActivation, self).prepare.original()

        @Activation.status.transition(source=STATUS.PREPARED, target='PAUSED')
        def pause(self):
            """
            Pause the task execution
            """

Note, that in the overriden `prepare` transition we calling base, non decorated function,
using `super(..)).prepare.original()`


Custom flow node
================

The `PausableView` node, have specified the `PausableViewActivation`
as the default activation class for the task, and overrides
`get_task_url` method to point default links to tasks in `PAUSED`
state to task execution page::


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


Pausable View
=============

`PausableViewMixin` calls the `activation.pause()` if user submits the
form using a button with `_pause` name::


    from django.http import HttpResponseRedirect
    from viewflow.flow.views import UpdateProcessView as BaseUpdateProcessView


    class PausableViewMixin(object):
        def form_valid(self, form):
            if '_pause' in self.request.POST:
                form.save()
                self.activation.pause()
                return HttpResponseRedirect(self.get_success_url())
            return super(PausableViewMixin, self).form_valid(form)


    class UpdateProcessView(PausableViewMixin, BaseUpdateProcessView):
        """
        UpdateProcessView with ability to pause a task
        """

We can add such button to the viewflow/flow/task.html::

    {% if activation.pause.can_proceed %}
    <button type="submit" name="_pause" class="btn btn-primary btn-lg">Save and Pause</button>
    {% endif %}


List of all paused task
=======================

`PausedListView` list all tasks in `PAUSED` state available for the user::
   
    class PausedListView(FlowViewPermissionMixin, generic.ListView):
        """List of puased flow tasks."""
        flow_cls = None

        context_object_name = 'task_list'
        template_name = 'viewflow/flow/paused_list.html'

        def get_queryset(self):
            return self.flow_cls.task_cls.objects.filter(
                process__flow_cls=self.flow_cls,
                owner=self.request.user,
                status='PAUSED'
            ).order_by('-created')

    urlpatterns = [
        ...
        url('^paused/$', PausedListView.as_view(flow_cls=IncomingMailFlow), name='paused'),
        ...
    ]

