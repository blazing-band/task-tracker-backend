from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class TaskStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


@dataclass
class Task:
    id: int
    user_id: int
    name: str
    text: str
    status: TaskStatus
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        """
        Convert Task attributes to dict for TaskDto construction.
        :return: dict with TaskDto fields
        """
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "status": self.status,
            "timestamp": self.timestamp,
        }
