# JSON 101

JSON storage and polymorphic user model

This sample shows how to use JSON storage and polymorphic proxy models, to implement efficient, single table authentication for different types of users.

## Quickstart

```bash
$ git clone https://github.com/viewflow/cookbook.git

$ python3 -m venv json101/venv
$ source json101/venv/activate

$ pip install json101/requirements.txt --extra-index-url=...
$ python3 json101/manage.py migrate
$ python3 json01/manage.py runserver
```

Navigate to http://127.0.0.1:8000

## Related documentation
- [JSON Storage](https://docs-next.viewflow.io/orm/json_storage.html)

## Most interesting files
- [models.py](./users/models.py) - Polymorphic user models definitions
