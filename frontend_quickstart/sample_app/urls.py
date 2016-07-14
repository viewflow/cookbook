from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    url('^$', TemplateView.as_view(template_name="sample_app/index.html"), name="index"),
]
