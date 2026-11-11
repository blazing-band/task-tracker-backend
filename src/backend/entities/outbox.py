from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class EventType(StrEnum):
    USER_CREATED = "UserCreated"
    DAILY_REPORT_CREATED = "DailyReportCreated"


class EventStatus(StrEnum):
    NEW = "NEW"
    SENT = "SENT"


@dataclass()
class Outbox:
    event_type: EventType
    payload: dict[str, Any]
    status: EventStatus = field(default=EventStatus.NEW)
    created_at: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)
