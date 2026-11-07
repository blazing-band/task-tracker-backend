from dishka import Provider
from dishka.integrations.fastapi import FastapiProvider

from .providers import (
    # CeleryProvider,  # TODO: celery is disabled for now
    InteractorsProvider,
    RedisProvider,
    RepositoriesProvider,
    ServicesProvider,
    SqlAlchemyProvider,
)


def get_providers() -> list[Provider]:
    return [
        FastapiProvider(),
        SqlAlchemyProvider(),
        ServicesProvider(),
        InteractorsProvider(),
        RepositoriesProvider(),
        RedisProvider(),
        # CeleryProvider(),
    ]
