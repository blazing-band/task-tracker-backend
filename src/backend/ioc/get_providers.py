from dishka import Provider
from dishka.integrations.fastapi import FastapiProvider

from .providers import (
    CeleryProvider,
    CeleryServicesProvider,
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
        CeleryProvider(),
    ]


def get_celery_providers() -> list[Provider]:
    return [
        CeleryServicesProvider(),
    ]
