from celery import Celery
from dishka import Provider, Scope, provide

from backend.settings import Settings


class CeleryProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_celery(self, settings: Settings) -> Celery:
        return Celery(broker=settings.rabbitmq.url)
