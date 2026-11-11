from collections.abc import Iterator

from confluent_kafka import Producer
from dishka import Provider, Scope, provide

from backend.kafka.daily_tasks_data_producer import DailyTasksDataProducer
from backend.settings import Settings


class KafkaProvider(Provider):
    daily_tasks_data_producer = provide(DailyTasksDataProducer, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_kafka_producer(self, settings: Settings) -> Iterator[Producer]:
        producer = Producer({"bootstrap.servers": settings.kafka.bootstrap_servers})
        yield producer
        producer.flush()
