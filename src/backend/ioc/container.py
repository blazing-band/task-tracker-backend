from dishka import AsyncContainer, Container, make_async_container, make_container

from backend.settings import Settings

from .get_providers import get_celery_providers, get_providers


def create_container(settings: Settings) -> AsyncContainer:
    return make_async_container(*get_providers(), context={Settings: settings})


def create_celery_container(settings: Settings) -> Container:
    return make_container(*get_celery_providers(), context={Settings: settings})
