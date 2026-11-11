from collections.abc import Iterator

from confluent_kafka import Producer
from dishka import Provider, Scope, provide

from backend.services import DailyReportProducer
from backend.settings import Settings


class KafkaProvider(Provider):
    daily_report_producer = provide(DailyReportProducer, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_kafka_producer(self, settings: Settings) -> Iterator[Producer]:
        producer = Producer({"bootstrap.servers": settings.kafka.bootstrap_servers})
        yield producer
        producer.flush()
