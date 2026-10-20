from dataclasses import dataclass
from datetime import datetime

from backend.entities import TaskStatus


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskDto:
    id: int
    name: str
    text: str
    status: TaskStatus
    timestamp: datetime
