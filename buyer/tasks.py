from celery import shared_task
from time import sleep
import logging

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    try:
        logger.info(f"Sum Task received with x={x} and y={y}")
        sleep(10)
        result = x + y
        logger.info(f"Task result: {result}")
        return result
    except Exception as e:
        logger.exception("An error occurred during task execution")
        raise e


@shared_task
def mult(x, y):
    try:
        logger.info(f"Multiply Task received with x={x} and y={y}")
        sleep(10)
        result = x * y
        logger.info(f"Task result: {result}")
        return result
    except Exception as e:
        logger.exception("An error occurred during task execution")
        raise e
