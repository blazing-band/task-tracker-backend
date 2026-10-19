from sqlalchemy import BigInteger, Column, String, Table

from backend.database import mapper_registry
from backend.entities import User

users_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String),
    Column("email", String, unique=True),
)


def map_user_table() -> None:
    mapper_registry.map_imperatively(User, users_table)
