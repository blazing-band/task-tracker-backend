from dishka import Provider, provide, Scope

from backend.repositories import UserRepository
from backend.repositories import RefreshTokenWhitelistRepository


class RepositoriesProvider(Provider):

    user_repository = provide(UserRepository, scope=Scope.REQUEST)
    refresh_token_whitelist_repository = provide(RefreshTokenWhitelistRepository, scope=Scope.REQUEST)
