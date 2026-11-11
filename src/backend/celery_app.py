from datetime import timedelta
from enum import StrEnum

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

from backend.settings import Settings


class CeleryTaskName(StrEnum):
    OUTBOX_RELAY = "outbox_relay"
    SEND_USER_REGISTERED_EMAIL = "email_sender.send_user_registered_email"
    SEND_USER_DAILY_REPORT_EMAIL = "email_sender.send_daily_report_email"
    SEND_USER_TASKS_STATISTICS = "backend.send_user_tasks_statistics"


class RabbitMqExchange(StrEnum):
    EMAIL = "email"


class RabbitMqQueues(StrEnum):
    REGISTRATION_EMAIL = "registration_email"
    DAILY_REPORT = "daily_report"


def create_celery(settings: Settings) -> Celery:
    celery_app = Celery("tasks", broker=settings.rabbitmq.url)
    celery_app.conf.task_acks_late = True
    celery_app.conf.task_reject_on_worker_lost = True
    # RabbitMQ 4.x forbids transient non-exclusive queues
    celery_app.conf.control_queue_exclusive = True
    celery_app.conf.event_queue_exclusive = True
    celery_app.conf.timezone = settings.app.app_timezone  # type: ignore[misc, assignment]
    celery_app.conf.broker_transport_options = {
        "confirm_publish": True
    }

    email_exchange = Exchange(RabbitMqExchange.EMAIL, type="direct", durable=True)

    celery_app.conf.task_queues = (
        Queue("celery"),
        Queue(
            RabbitMqQueues.REGISTRATION_EMAIL,
            email_exchange,
            routing_key=RabbitMqQueues.REGISTRATION_EMAIL,
            durable=True,
        ),
        Queue(
            RabbitMqQueues.DAILY_REPORT,
            email_exchange,
            routing_key=RabbitMqQueues.DAILY_REPORT,
            durable=True,
        ),
    )

    celery_app.conf.task_routes = {
        CeleryTaskName.SEND_USER_REGISTERED_EMAIL: {
            "queue": RabbitMqQueues.REGISTRATION_EMAIL,
            "exchange": RabbitMqExchange.EMAIL,
            "routing_key": RabbitMqQueues.REGISTRATION_EMAIL,
        },
        CeleryTaskName.SEND_USER_DAILY_REPORT_EMAIL: {
            "queue": RabbitMqQueues.DAILY_REPORT,
            "exchange": RabbitMqExchange.EMAIL,
            "routing_key": RabbitMqQueues.DAILY_REPORT,
        },
    }

    celery_app.conf.beat_schedule = {
        "send-user-created-email": {
            "task": CeleryTaskName.OUTBOX_RELAY,
            "schedule": timedelta(seconds=2)
        },
        "send-user-tasks-statistics-every-midnight": {
            "task": CeleryTaskName.SEND_USER_TASKS_STATISTICS,
            "schedule": crontab(minute=0, hour=0),
        },
    }

    return celery_app
