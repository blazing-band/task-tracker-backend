from sqlalchemy import Table, Column, UUID, Enum, JSON, func, DateTime

from backend.database.registry import mapper_registry
from backend.entities import Outbox, EventType, EventStatus

outbox_table = Table(
    "outbox",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column(
        "event_type",
        Enum(
            EventType, create_constraint=True, native_enum=False
        ),
        nullable=False,
    ),
    Column("payload", JSON, nullable=False),
    Column(
        "status",
        Enum(
            EventStatus, create_constraint=True, native_enum=False
        ),
        server_default=EventStatus.NEW.value,
    ),
    Column(
        "created_at",
        DateTime,
        server_default=func.now(),
    )
)


def map_outbox_table() -> None:
    mapper_registry.map_imperatively(Outbox, outbox_table)
