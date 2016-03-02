===========================
Viewflow Pro Subrocess Demo
===========================

This recipe demonstrates how to use Subprocess in the django-viewflow library

.. image:: .screenshot.png
   :width: 400px


Run this sample with::

    tox --notest -i https://pypi.viewflow.io/<licence_id>/simple/
    tox python manage.py migrate
    tox python manage.py createsuperuser
    tox python manage.py runserver


Navigate to http://127.0.0.1:8000
