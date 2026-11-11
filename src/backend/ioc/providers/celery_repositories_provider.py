from dishka import Provider, Scope, provide

from backend.repositories import SyncTaskRepository


class CeleryRepositoriesProvider(Provider):
    task_repository = provide(SyncTaskRepository, scope=Scope.REQUEST)
