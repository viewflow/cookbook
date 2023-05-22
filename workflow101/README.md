# Workflow 101

Hello World workflow sample

## Online demo

https://demo-next.viewflow.io/workflow/

## Quickstart

```bash
$ git clone https://github.com/viewflow/cookbook.git

$ python3 -m venv workflow101/venv
$ source workflow101/venv/activate

$ pip install workflow101/requirements.txt --extra-index-url=...
$ python3 workflow101/manage.py migrate
$ python3 workflow101/manage.py createsuperuser
$ python3 workflow101/manage.py loaddata workflow101/fixtures/*.json
$ python3 workflow101/manage.py runserver
```

Navigate to http://127.0.0.1:8000


## Related documentation

- [BPMN Workflow](https://docs.viewflow.io/bpmn/index.html)
- [Site and Application Viewsets](https://docs.viewflow.io/-frontend/site.html)

## Most interesting files

- [urls.py](./config/urls.py) - Setup base site urls
- [flows.py](./helloworld/flows.py) - Hello world workflow definition
