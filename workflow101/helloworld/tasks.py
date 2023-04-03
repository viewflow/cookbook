import os
from codecs import open
from celery import shared_task
from viewflow.contrib.celery import Job


@shared_task
def send_hello_world_request(activation_ref):
    """
    Sends a hello world message.

    This task is executed asynchronously by Celery when the send step in the
    `HelloWorldFlow` process is reached.

    activation_ref : str
        The reference to the activation data of the `HelloWorldProcess` instance
        to which this task is associated.

    """
    with Job.activate(activation_ref) as activation:
        with open(os.devnull, "w", encoding="utf-8") as world:
            world.write(activation.process.text)
