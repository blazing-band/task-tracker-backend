"""Entrypoint for kafka consumer"""
from backend.kafka import KafkaConsumer
from backend.settings import load_settings


if __name__ == "__main__":
    settings = load_settings()
    consumer = KafkaConsumer(settings)
    consumer.consume()
    # TODO maybe to use inbox. Put kafka message in inbox table if not exssits, else acknolege kafka that message alredy prpcedured
