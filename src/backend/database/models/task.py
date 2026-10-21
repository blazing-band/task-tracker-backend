from sqlalchemy import BigInteger, Column, DateTime, Enum, ForeignKey, String, Table, Text, func
from sqlalchemy.orm import relationship

from backend.entities import Task, TaskStatus, User

from ..registry import mapper_registry

task_table = Table(
    "task",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("user_id", BigInteger, ForeignKey("user.id"), nullable=False),
    Column("name", String(255), nullable=False),
    Column("text", Text, nullable=False),
    Column("status", Enum(TaskStatus), nullable=False, server_default=TaskStatus.IN_PROGRESS.value),
    Column("timestamp", DateTime, nullable=False, server_default=func.now()),
)


def map_task_table() -> None:
    mapper_registry.map_imperatively(Task, task_table, properties={"user": relationship(User, back_populates="tasks")})
