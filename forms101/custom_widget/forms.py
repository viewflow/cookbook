from viewflow.forms import ModelForm, Layout, Row, InlineFormSetField
from django.forms import modelform_factory, FileInput

from . import models


class AttachmentForm(ModelForm):
    class Meta:
        model = models.Attachment
        fields = ["name", "image"]
        # widgets = {"image": FileInput(attrs={"tag": "my-file-upload"})}


class EmailForm(ModelForm):
    emails = InlineFormSetField(
        parent_model=models.Email,
        model=models.Attachment,
        form=AttachmentForm,
        label="Email attachments",
        can_delete=False,
    )

    layout = Layout(
        "subject",
        Row("from_email", "to_email"),
        "message",
        "emails",
    )

    class Meta:
        model = models.Email
        fields = ["subject", "message", "from_email", "to_email"]

    def is_multipart(self):
        return True


# todo
# 1. fix undefined inside the input
# 2 .found js sample
# 3. vite custom
# 4. custom template with js included
# 5. fix form enc type
