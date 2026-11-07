from enum import StrEnum

from celery import Celery
from kombu import Exchange, Queue

from backend.settings import RabbitmqSettings


class CeleryTaskName(StrEnum):
    SEND_USER_REGISTERED_EMAIL = "email_sender.send_user_registered_email"


class RabbitMqExchange(StrEnum):
    EMAIL = "email"


class RabbitMqQueues(StrEnum):
    REGISTRATION_EMAIL = "registration_email"


def create_celery(rabbitmq_settings: RabbitmqSettings) -> Celery:
    celery_app = Celery("tasks", broker=rabbitmq_settings.url)
    celery_app.conf.task_acks_late = True
    celery_app.conf.task_reject_on_worker_lost = True
    # RabbitMQ 4.x forbids transient non-exclusive queues
    celery_app.conf.control_queue_exclusive = True
    celery_app.conf.event_queue_exclusive = True

    email_exchange = Exchange(RabbitMqExchange.EMAIL, type="direct", durable=True)

    celery_app.conf.task_queues = (
        Queue(
            RabbitMqQueues.REGISTRATION_EMAIL,
            email_exchange,
            routing_key=RabbitMqQueues.REGISTRATION_EMAIL,
            durable=True,
        ),
    )

    celery_app.conf.task_routes = {
        CeleryTaskName.SEND_USER_REGISTERED_EMAIL: {
            "queue": RabbitMqQueues.REGISTRATION_EMAIL,
            "exchange": RabbitMqExchange.EMAIL,
            "routing_key": RabbitMqQueues.REGISTRATION_EMAIL,
        },
    }

    return celery_app
