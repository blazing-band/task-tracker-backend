from dishka import Provider
from dishka.integrations.fastapi import FastapiProvider

from .providers import (
    CeleryProvider,
    CeleryRepositoriesProvider,
    CeleryServicesProvider,
    InteractorsProvider,
    KafkaProvider,
    RedisProvider,
    RepositoriesProvider,
    ServicesProvider,
    SqlAlchemyProvider,
    SyncSqlAlchemyProvider,
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
        SyncSqlAlchemyProvider(),
        CeleryRepositoriesProvider(),
        KafkaProvider(),
    ]
