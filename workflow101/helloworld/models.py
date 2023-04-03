from django.utils.translation import gettext_lazy as _

from viewflow import jsonstore
from viewflow.workflow.models import Process


class HelloWorldProcess(Process):
    """
    A hello world message request process data.

    This model extends the base viewflow `Process` model to store the
    information related to a hello world message request process, including
    the message text and its approval status.

    Fields:
        text (jsonstore.CharField): The message text to be sent to the world.
        approved (jsonstore.BooleanField): The approval status of the message.

    """

    text = jsonstore.CharField(_("Message"), max_length=50)
    approved = jsonstore.BooleanField(_("Approved"), default=False)

    class Meta:
        proxy = True
        verbose_name = _("World Request")
        verbose_name_plural = _("World Requests")
