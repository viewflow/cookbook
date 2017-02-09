==============================================
Quick start with frontend from django-material
==============================================

This recipe demonstrates how to setup frontend with django-material
and create a simple fronted module


1. Setup django and django-material::

    pip install django django-material

2. Create a new django project::

    django_admin.py startproject frontend_quickstart


3. Start the new django app::

    python manage.py startapp sample_app

4. Configure the project settings

Include 'material', 'material.frontend', and our 'sample_app' into INSTALLED_APPS setting::

    INSTALLED_APPS = (
        'material',
        'material.frontend',
        ...
        'sample_app.apps.SampleAppConfig')

5. Add frontend urls into global urlconf module at urls.py::

    from material.frontend import urls as frontend_urls

    urlpatterns = [
        ...
        url(r'^admin/', include(admin.site.urls)),
        url(r'', include(frontend_urls)),
    ]


6. To mark application as frontend module add ModuleMixin to the SampleAppConfig class::

    from django.apps import AppConfig
    from material.frontend.apps import ModuleMixin


    class SampleAppConfig(ModuleMixin, AppConfig):
        name = 'sample_app'
        icon = '<i class="material-icons">extension</i>'

7. Create module sample_app/urls.py

You don't need to include this `urls.py` into global `ROOT_URLCONF`. The `frontend.urls` would discover module urls automatically::

    from django.views.generic import TemplateView
    from django.conf.urls import url

    urlpatterns = [
        url('^$', TemplateView.as_view(template_name="sample_app/index.html"), name="index"),
    ]

8. Put `index.html` into new `sample_app/templates/sample_app/` directory::

    {% extends 'material/frontend/base_module.html' %}

    {% block content %}
    <div class="left-panel">
        <div class="card">
            <div class="card-content">
                <div class="card-title black-text">{{ current_module.label }}</div>
                <h5>Installed modules</h5>
                <ul>
                    {% for module in modules %}
                    <li>{{ module.label }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
    {% endblock %}


9. Start the sample

Create sqlite database::

    python manage.py migrate

Create a super user with login `admin` and password `admin`::

    tox python manage.py createsuperuser

Start the webserver::

    tox python manage.py runserver 0.0.0.0 8000


Navigate to http://127.0.0.1:8000 to see the result
