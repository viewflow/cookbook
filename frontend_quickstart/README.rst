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

    python manage.py sample_app

4. Configure the project settings

Include 'material', 'material.frontend', 'easy_pjax' and our 'sample_app' into INSTALLED_APPS setting::

    INSTALLED_APPS = (
        'material',
        'material.frontend',
        'easy_pjax',
        ...
        'sample_app')

Add `material.frontend.context_processors.modules` into `context_processor` setting::

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'material.frontend.context_processors.modules',
                ],
            },
        },
    ]


5. Add frontend urls into global urlconf module at urls.py::

    from material.frontend import urls as frontend_urls

    urlpatterns = [
        ...
        url(r'^admin/', include(admin.site.urls)),
        url(r'', include(frontend_urls)),
    ]


5. To create a new module make a `modules.py` file, inside sample_app/ directory, with following content::

    from material.frontend import Module


    class Sample(Module):
        icon = 'mdi-image-compare'

6. Put `index.html` into new `sample_app/templates/sample/` directory::

    {% extends 'material/frontend/base_module.html' %}

    {% block content %}
    <div class="row">
        <div class="col s4">
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
    </div>
    {% endblock %}


7. Start the sample

Create sqlite database::

    python manage.py migrate

Create a super user with login `admin` and password `admin`::

    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin3', 'admin@example.com', 'admin3')" | python manage.py shell

Start the webserver::

    tox python manage.py runserver 0.0.0.0 8000


Navigate to http://127.0.0.1:8000 to see the result