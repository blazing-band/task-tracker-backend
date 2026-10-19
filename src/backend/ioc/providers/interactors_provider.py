from dishka import Provider, Scope, provide

from backend.interactors import CreateSession, CreateUser, Logout


class InteractorsProvider(Provider):
    create_user = provide(CreateUser, scope=Scope.REQUEST)
    create_session = provide(CreateSession, scope=Scope.REQUEST)
    logout = provide(Logout, scope=Scope.REQUEST)
