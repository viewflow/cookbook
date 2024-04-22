from django.contrib import messages
from django.http import HttpResponseBadRequest, QueryDict, JsonResponse
from django.views import generic
from viewflow.views import FormLayoutMixin
from viewflow.forms import FormDependentSelectMixin, FormAjaxCompleteMixin
from .user_form import UserForm
from . import COUNTRY_CHOICES


class CheckoutFormView(generic.FormView):
    initial = {
        "postcode": "1206610",
        "city": "12060",
        "country": "1",
    }

    def options(self, *args, **kwargs):
        if "HTTP_X_REQUEST_SELECT_OPTIONS" in self.request.META:
            query = self.request.META.get("HTTP_X_REQUEST_SELECT_OPTIONS")
            options = QueryDict(query, encoding=self.request.encoding)
            field = options.get("field", "")
            query = options.get("query")

            if field == "city":
                from cookbook.crud101.atlas.models import Country

                country_names = [
                    country[1]
                    for country in COUNTRY_CHOICES
                    if str(country[0]) == query
                ]
                if not country_names:
                    return

                cities = Country.objects.get(name=country_names[0]).cities.all()

                return JsonResponse(
                    {
                        "data": [
                            {
                                "name": "",
                                "options": {
                                    "value": f"{query}{city.pk}",
                                    "label": city.name,
                                    "selected": False,
                                },
                            }
                            for city in cities
                        ]
                    }
                )

            elif field == "post_code":
                return JsonResponse(
                    {
                        "data": [
                            {
                                "name": "",
                                "options": {
                                    "value": query + "10",
                                    "label": query + "10",
                                    "selected": False,
                                },
                            },
                            {
                                "name": "",
                                "options": {
                                    "value": query + "20",
                                    "label": query + "20",
                                    "selected": False,
                                },
                            },
                            {
                                "name": "",
                                "options": {
                                    "value": query + "30",
                                    "label": query + "30",
                                    "selected": False,
                                },
                            },
                        ]
                    }
                )

        return HttpResponseBadRequest("Unknown request")


class CreateUserView(
    FormLayoutMixin,
    FormDependentSelectMixin,
    FormAjaxCompleteMixin,
    generic.CreateView,
):
    form_class = UserForm
    template_name = "forms/form.html"
    extra_context = {"title": "Create user form", "button": "Submit"}

    def form_valid(self, *args, **kwargs):
        response = super().form_valid(*args, **kwargs)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "User created!",
            fail_silently=True,
        )
        return response
