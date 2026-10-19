from datetime import datetime
from enum import StrEnum


class TaskStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task:
    id: int
    user_id: int
    name: str
    text: str
    status: TaskStatus
    timestamp: datetime