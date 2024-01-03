# Legacy DB

## Quickstart

Get and install PostgreSQL Demo Database - https://postgrespro.com/education/demodb

```bash
$ git clone https://github.com/viewflow/cookbook.git

$ python3 -m venv legacy_db/venv
$ source legacy_db/venv/bin/activate

$ pip install fsm101/requirements.txt --extra-index-url=...
$ python3 legacy_db/manage.py migrate
$ python3 legacy_db/manage.py runserver
```

Navigate to http://127.0.0.1:8000

## Related documentation
- [Composite FK field](http://docs.viewflow.io/orm/composite_fk.html)

## Most interesting files
- [routers.py](./config/routers.py) - DB Router to integrate demo db
- [models.py](./airdata/models.py) - Model definitions for the demo database
