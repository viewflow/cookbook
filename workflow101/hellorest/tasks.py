import os
from codecs import open
from celery import shared_task
from viewflow.contrib.celery import Job


@shared_task
def send_hello_world_request(activation_ref):
    with Job.activate(activation_ref) as activation:
        with open(os.devnull, "w", encoding='utf-8') as world:
            world.write(activation.process.text)
