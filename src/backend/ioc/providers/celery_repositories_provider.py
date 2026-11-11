from dishka import Provider, Scope, provide

from backend.repositories import SyncTaskRepository, SyncOutboxRepository


class CeleryRepositoriesProvider(Provider):
    task_repository = provide(SyncTaskRepository, scope=Scope.REQUEST)
    outbox_repository = provide(SyncOutboxRepository, scope=Scope.REQUEST)
