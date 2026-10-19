from dishka import AsyncContainer, make_async_container

from .get_providers import get_providers


def get_container() -> AsyncContainer:
    return make_async_container(*get_providers())
