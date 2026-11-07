from collections.abc import Iterator

from celery import Celery
from dishka import Provider, Scope, provide

from backend.celery_app import create_celery
from backend.settings import Settings


class CeleryProvider(Provider):
    @provide(scope=Scope.APP)
    def get_celery(self, settings: Settings) -> Iterator[Celery]:
        celery = create_celery(settings.rabbitmq)
        yield celery
        celery.close()
