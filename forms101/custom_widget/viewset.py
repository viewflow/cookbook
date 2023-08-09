from viewflow.urls import ModelViewset
from . import models, forms


class EmailViewset(ModelViewset):
    model = models.Email
    list_columns = ("pk", "sent_at", "subject", "from_email", "to_email")
    form_class = forms.EmailForm
