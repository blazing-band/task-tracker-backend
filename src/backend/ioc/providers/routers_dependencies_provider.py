from dishka import Provider, provide, Scope

from backend.routers.identity_provider import IdentityProvider


class RoutersProvider(Provider):

    identity_provider = provide(IdentityProvider, scope=Scope.REQUEST)
