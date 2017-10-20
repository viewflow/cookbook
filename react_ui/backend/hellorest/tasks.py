import os
from codecs import open

from celery import shared_task
from viewflow.flow import flow_job


@shared_task
@flow_job
def send_hello_world_request(activation):
    with open(os.devnull, "w", encoding='utf-8') as world:
        world.write(activation.process.text)
