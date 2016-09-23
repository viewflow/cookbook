=====================
Viewflow Rest Backend
=====================

Create a virtual env and install dependencies::

  $ virtualenv --python=python3.4 env
  $ . env/bin/activate
  $ pip install django djangorestframework viewflow


Let's start with basic app::

  $ django-admin startproject config
  $ ./manage.py startapp hellorest

Add `rest_framework.authtoken`, and `hellorest` to the settings.INSTALLED_APPS
