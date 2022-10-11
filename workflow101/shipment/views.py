from django.http import HttpResponseRedirect
from django.views import generic
from viewflow.workflow.flow.views import TaskSuccessUrlMixin

from .forms import ShipmentForm
from .models import Insurance


class StartView(TaskSuccessUrlMixin, generic.CreateView):
    form_class = ShipmentForm
    template_name = 'viewflow/workflow/start.html'

    def form_valid(self, form):
        self.object = form.save()

        self.request.activation.process.artifact = self.object

        self.request.activation.execute()
        return HttpResponseRedirect(self.get_success_url())


class ShipmentView(TaskSuccessUrlMixin, generic.UpdateView):
    template_name = 'viewflow/workflow/task.html'

    def get_object(self):
        return self.request.activation.process.artifact

    def form_valid(self, form):
        self.object = form.save()

        self.request.activation.process.artifact = self.object

        self.request.activation.execute()
        return HttpResponseRedirect(self.get_success_url())


class InsuranceView(TaskSuccessUrlMixin, generic.CreateView):
    model = Insurance
    template_name = 'viewflow/workflow/task.html'
    fields = ["company_name", "cost"]

    def form_valid(self, form):
        self.object = form.save()

        shipment = self.request.activation.process.artifact
        shipment.insurance = self.object
        shipment.save(update_fields=["insurance"])

        self.request.activation.execute()
        return HttpResponseRedirect(self.get_success_url())
