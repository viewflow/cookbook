# Dashboard

Quick material-design dashboard with Chart.js

This demo shows how to quickly connect a single view to the site menu and use base dashboard prepared templates.

## Online demo

https://demo-next.viewflow.io/dashboard/dashboard/

## Quickstart

```bash
$ git clone https://github.com/viewflow/cookbook.git

$ python3 -m venv dashboard/venv
$ source dashboard/venv/activate

$ pip install dashboard/requirements.txt --extra-index-url=...
$ python3 crud101/manage.py migrate
$ python3 crud101/manage.py runserver
```

Navigate to http://127.0.0.1:8000

## Related documentation

- [Site and Application Viewsets](https://docs-next.viewflow.io/-frontend/site.html)
- [Chart.js documentation](https://www.chartjs.org/docs/latest/)

## Most interesting files
- [urls.py](./config/urls.py) - Setup base site urls
- [dashboard.html](./board/templates/board/dashboard.html) - Dashboard template
