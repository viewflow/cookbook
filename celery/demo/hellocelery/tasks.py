from celery import shared_task
from celery.utils.log import get_task_logger

from viewflow.flow import flow_job


logger = get_task_logger(__name__)


@shared_task
@flow_job
def send_hello_world_request(activation):
    logger.info(activation.process.text)