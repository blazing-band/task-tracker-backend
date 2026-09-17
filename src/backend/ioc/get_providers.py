from dishka import Provider

from .providers import (
    SettingsProvider, SqlAlchemyProvider, InteractorsProvider, ServicesProvider, RepositoriesProvider,

)
from .providers import RedisProvider


def get_providers() -> list[Provider]:
    return [
        SettingsProvider(),
        SqlAlchemyProvider(),
        ServicesProvider(),
        InteractorsProvider(),
        RepositoriesProvider(),
        RedisProvider()
    ]
