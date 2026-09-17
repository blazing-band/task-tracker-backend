from dishka import make_async_container, AsyncContainer

from .get_providers import get_providers


def get_container() -> AsyncContainer:
    return make_async_container(*get_providers())

