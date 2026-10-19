from dishka import Provider, Scope, provide

from backend.repositories import RefreshTokenWhitelistRepository, UserRepository


class RepositoriesProvider(Provider):
    user_repository = provide(UserRepository, scope=Scope.REQUEST)
    refresh_token_whitelist_repository = provide(RefreshTokenWhitelistRepository, scope=Scope.REQUEST)
