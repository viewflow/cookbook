Custom widget
=============

Install dependencies from npm
-----------------------------

npm init -y
npm install vite typescript <your_js_library>


Write WebComponents wrapper
---------------------------

..code:

    class MyComponent extends HTMLElement {
      connectedCallback() {
        // TODO initialization
      }

      disconnectedCallback() {
        // TODO clear resources and event listeners if required
      }
    }

    window.customElements.define('my-component', MyComponent);



Configure Vite
--------------

See vite.config.ts and tsconfig.json for the reference

Add following scripts to packages.json

  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build"
  },


npm run build

Set Django settings
-------------------

List your `static` and `templates` folders in the corresponding Django settings

..code: python

    STATICFILES_DIRS = [BASE_DIR / "static"]
    TEMPLATES = [
    {
        ...
        "DIRS": [
            BASE_DIR / "templates",
        ],
        ...
    }


Include custom js in the base template
--------------------------------------

`templates/viewflow/base.html`

..code: html

    {% extends 'viewflow/base_page.html' %}{% load static %}

    {% block extrahead %}
    <script src="{% static 'js/my_components.min.js' %}" type="text/javascript"></script>
    {% endblock %}


Register custom form widget
---------------------------

TODO

Use custom widget in a form
---------------------------

TODO

Running demo
------------

Run `npm run build` to create compiled source code and then as usual

..code: bash

     ./manage.py makemigrations
     ./manage.py migrate
     ./manage.py createsuperuser
     ./manage.py runserver

