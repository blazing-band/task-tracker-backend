import json

from confluent_kafka import KafkaException, Consumer

from backend.settings import Settings
from backend.tasks import send_user_registered_email


class KafkaConsumer:

    def __init__(self, settings: Settings) -> None:
        self.consumer = Consumer(
            {
                "bootstrap.servers": settings.kafka.bootstrap_servers,
                "group.id": "daily_tasks_report",
                "enable.auto.commit": "false"
            }
        )
        self.topic = "daily_tasks_report"

    def consume(self) -> None:
        try:
            self.consumer.subscribe([self.topic])

            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue

                if msg.error():
                    # TODO to think about how to handle kafka exception in consumer process
                    raise KafkaException(msg.error())

                payload = json.loads(msg.value().decode("utf-8"))  # type: ignore[union-attr]
                send_user_registered_email.delay(**payload)  # type: ignore[attr-defined]
                self.consumer.commit()

        finally:
            self.consumer.close()
