from django.views import generic
from django.http import HttpResponseRedirect

from viewflow.workflow.flow.views import TaskSuccessUrlMixin
from .models import Decision


class DecisionView(TaskSuccessUrlMixin, generic.CreateView):
    model = Decision
    fields = ['decision']
    template_name = 'viewflow/workflow/task.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.user = self.request.user
        self.object.process = self.request.activation.process
        self.object.save()

        self.request.activation.execute()
        # self.success('Task {task} has been completed.')

        return HttpResponseRedirect(self.get_success_url())
