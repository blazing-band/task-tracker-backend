from confluent_kafka import Consumer, KafkaException

from backend.settings import Settings


class DailyReportConsumer:

    def __init__(self, settings: Settings) -> None:
        self.consumer = Consumer(
            {
                "bootstrap.servers": settings.kafka.bootstrap_servers,
                "group_id": "daily_tasks_report"
            }
        )
        self.topic = "daily_tasks_report"

    def consume(self):
        try:
            self.consumer.subscribe([self.topic])

            while True:
                msg = self.consumer.poll(1.0)
                if msg is None: continue

                if msg.error():
                    raise KafkaException(msg.error())
                else:


        finally:
            self.consumer.close()
