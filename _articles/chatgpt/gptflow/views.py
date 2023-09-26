from django.http import HttpResponseRedirect
from django.views import generic
from viewflow.views import FormLayoutMixin
from viewflow.workflow.flow.views import (
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
    UpdateArtifactView,
)
from .forms import ArticleSelectForm
from .models import Article


class CreateArticleView(
    FormLayoutMixin,
    SuccessMessageMixin,
    TaskSuccessUrlMixin,
    TaskViewTemplateNames,
    generic.CreateView,
):
    model = Article
    fields = ["content"]
    template_name = "gptflow/create_article.html"

    def form_valid(self, form):
        article = form.save(commit=False)
        article.summary = self.request.activation.process.artifact
        article.model = "Claude"
        article.save()
        self.request.activation.execute()
        return HttpResponseRedirect(self.get_success_url())


class SelectArticleView(UpdateArtifactView):
    form_class = ArticleSelectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["summary"] = self.request.activation.process.artifact
        return kwargs
