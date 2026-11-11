"""Celery worker entrypoint"""

from typing import Any

from celery.signals import worker_shutdown
from dishka.integrations.celery import setup_dishka

from backend.celery_app import create_celery
from backend.database import map_tables
from backend.ioc import create_celery_container
from backend.settings import load_settings

settings = load_settings()
# Entities are mapped imperatively; without this ORM queries on Task/User fail
map_tables()

celery_app = create_celery(settings.rabbitmq)
celery_app.conf.include = ["backend.tasks"]

container = create_celery_container(settings)
setup_dishka(container, celery_app)


@worker_shutdown.connect
def close_container(**kwargs: Any) -> None:
    container.close()
