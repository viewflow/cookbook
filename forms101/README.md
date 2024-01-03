# Forms 101

Various form options samples

## Online demo

https://demo.viewflow.io/forms/

## Quickstart

```bash
$ git clone https://github.com/viewflow/cookbook.git

$ python3 -m venv forms101/venv
$ source forms101/venv/bin/activate

$ pip install forms101/requirements.txt --extra-index-url=...
$ python3 forms101/manage.py migrate
$ python3 forms101/manage.py runserver
```

Navigate to http://127.0.0.1:8000

## Related documentation

- [Material Forms](https://docs.viewflow.io/forms/index.html)

## Most interesting files
- [viewset.py](./forms/viewset.py) - Class-based URL configuration
- [bank_form.py](./forms/bank_form.py) - Complex form layout sample
- [hospital_form.py](./forms/hospital_form.py) - Checkbox lists render options and dynamic formsets
- [login_form.py](./forms/login_form.py) - Basic widgets with custom icons
- [signup_form.py](./forms/signup_form.py) - Nested form sample
- [wizard_form.py](./forms/wizard_form.py) - Multistep form sample
