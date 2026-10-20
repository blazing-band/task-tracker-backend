from sqlalchemy import BigInteger, Column, String, Table
from sqlalchemy.orm import relationship

from backend.entities import User, Task

from ..registry import mapper_registry

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("username", String, unique=True, nullable=True),
    Column("password", String, nullable=True),
    Column("email", String, unique=True, nullable=True),
)


def map_user_table() -> None:
    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "tasks": relationship(Task, back_populates="user")
        }
    )
