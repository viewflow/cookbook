============================
Viewflow Pro Helloworld Demo
============================

Run this sample with::

    virtualenv env --python=python2.7
    source env/bin/activate
    pip install -i https://pypi.viewflow.io/<licence_id>/simple/
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

And run on other console::

    celery worker -A config.celery_app -l debug


Navigate to http://127.0.0.1:8000
