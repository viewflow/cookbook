from django.views import generic
from django.http import HttpResponseRedirect

from viewflow.flow.views import UpdateProcessView as BaseUpdateProcessView
from viewflow.flow.views.mixins import FlowViewPermissionMixin


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
