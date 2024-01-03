# CRUD 101

Admin-style CRUD application

This demo shows how to create a quick CRUD frontend.

## Online demo

https://demo.viewflow.io/atlas/

## Quickstart

```bash
$ git clone https://github.com/viewflow/cookbook.git --depth=1

$ python3 -m venv cookbook/crud101/venv
$ source cookbook/crud101/venv/bin/activate

$ pip install -r cookbook/crud101/requirements.txt --extra-index-url https://pypi.viewflow.io/<licence_id>/simple/
$ python3 cookbook/crud101/manage.py migrate
$ python3 cookbook/crud101/manage.py loaddata cookbook/crud101/atlas/fixtures/*.json
$ python3 cookbook/crud101/manage.py runserver
```

Navigate to http://127.0.0.1:8000

 **login** - admin
 **password** - admin

## Related documentation

- [Site and Application Viewsets](https://docst.viewflow.io/-frontend/site.html)
- [CRUD Viewset](https://docs.viewflow.io/frontend/crud.html)

## Most interesting files

- [urls.py](./config/urls.py) - Setup base site urls
- [viewset.py](./atlas/viewset.py) - CRUD viewset options
