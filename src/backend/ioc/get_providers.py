from dishka import Provider

from .providers import (
    # CeleryProvider,  # TODO: celery is disabled for now
    InteractorsProvider,
    RedisProvider,
    RepositoriesProvider,
    ServicesProvider,
    SettingsProvider,
    SqlAlchemyProvider,
)


def get_providers() -> list[Provider]:
    return [
        SettingsProvider(),
        SqlAlchemyProvider(),
        ServicesProvider(),
        InteractorsProvider(),
        RepositoriesProvider(),
        RedisProvider(),
        # CeleryProvider(),
    ]
