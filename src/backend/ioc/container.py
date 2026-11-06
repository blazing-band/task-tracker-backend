from dishka import AsyncContainer, make_async_container

from .get_providers import get_providers

from backend.settings import Settings


def create_container(settings: Settings) -> AsyncContainer:
    return make_async_container(*get_providers(), context={Settings: settings})
