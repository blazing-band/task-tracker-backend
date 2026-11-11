import json
import logging
from dataclasses import asdict

from confluent_kafka import KafkaError, Message, Producer

from backend.dtos import DailyReportDto
from backend.settings import Settings

logger = logging.getLogger(__name__)


class DailyReportProducer:
    def __init__(self, producer: Producer, settings: Settings) -> None:
        self.producer = producer
        self.topic = settings.kafka.daily_report_topic

    def send(self, report: DailyReportDto) -> None:
        self.producer.produce(
            self.topic,
            key=report.user.email.encode(),
            value=json.dumps(asdict(report), ensure_ascii=False).encode(),
            on_delivery=self._on_delivery,
        )
        # Serve delivery callbacks of earlier messages and free the local queue
        self.producer.poll(0)

    def flush(self, timeout: float = 30) -> None:
        """Wait until all sent reports are delivered; raise if some are not."""
        not_delivered = self.producer.flush(timeout)
        if not_delivered:
            raise RuntimeError(f"{not_delivered} daily reports were not delivered to Kafka")

    @staticmethod
    def _on_delivery(err: KafkaError | None, msg: Message) -> None:
        if err is not None:
            logger.error("Failed to deliver daily report to %s: %s", msg.topic(), err)
