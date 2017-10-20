=======================
REST Workflow UI Sample
=======================

To run the demo, you need to start three separate processes

Frontend
========

   $ cd frontend/
   $ npm start


Django Server
=============

    $ cd backend/
    $ tox python manage.py runserver 0.0.0.0:8000


Celery Worker
=============

    $ cd backend/
    $ tox -e celery
