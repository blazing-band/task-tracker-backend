from dishka import AsyncContainer, make_async_container

from backend.settings import Settings

from .get_providers import get_providers


def create_container(settings: Settings) -> AsyncContainer:
    return make_async_container(*get_providers(), context={Settings: settings})
