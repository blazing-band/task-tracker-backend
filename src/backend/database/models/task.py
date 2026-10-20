from sqlalchemy import Table, Column, String, Text, BigInteger, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from ..registry import mapper_registry
from backend.entities import Task, User, TaskStatus

task_table = Table(
    "task",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("user_id", BigInteger, ForeignKey("user.id"), nullable=False),
    Column("name", String(255), nullable=False),
    Column("text", Text, nullable=False),
    Column("status", Enum(TaskStatus), nullable=False),
    Column("timestamp", DateTime, nullable=False)


)


def map_task_table() -> None:
    mapper_registry.map_imperatively(
        Task,
        task_table,
        properties={
            "user": relationship(User, back_populates="tasks")
        }
    )
