# CRUD 101

Admin-style CRUD application

This demo shows how to create a quick CRUD frontend.

## Online demo

https://demo-next.viewflow.io/atlas/

## Quickstart

```bash
$ git clone https://github.com/viewflow/cookbook.git

$ python3 -m venv crud101/venv
$ source crud101/venv/activate

$ pip install crud101/requirements.txt --extra-index-url=...
$ python3 crud101/manage.py migrate
$ python3 crud101/manage.py loaddata crud101/atlas/fixtures/*.json
$ python3 crud101/manage.py runserver
```

Navigate to http://127.0.0.1:8000

 **login** - admin
 **password** - admin

## Related documentation

- [Site and Application Viewsets](https://docs-next.viewflow.io/-frontend/site.html)
- [CRUD Viewset](https://docs-next.viewflow.io/frontend/crud.html)

## Most interesting files

- [urls.py](./config/urls.py) - Setup base site urls
- [viewset.py](./atlas/viewset.py) - CRUD viewset options
