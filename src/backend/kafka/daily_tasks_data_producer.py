import json
import logging
from dataclasses import asdict

from confluent_kafka import Producer

from backend.dtos import DailyReportDto
from backend.settings import Settings

logger = logging.getLogger(__name__)


class DailyTasksDataProducer:
    def __init__(self, producer: Producer) -> None:
        self.producer = producer
        self.topic = "daily_tasks_data"

    def send(self, report: DailyReportDto) -> None:
        self.producer.produce(
            self.topic,
            value=json.dumps(asdict(report)).encode(),
        )


