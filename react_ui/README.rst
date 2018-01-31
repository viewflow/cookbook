=======================
REST Workflow UI Sample
=======================

To run the demo, you need to start three separate processes

Frontend
========

.. code:: bash

    $ cd frontend/
    $ npm install
    $ npm start


Django Server
=============

.. code:: bash

    $ cd backend/
    $ tox python manage.py runserver 0.0.0.0:8000


Celery Worker
=============

.. code:: bash

    $ cd backend/
    $ tox -e celery
