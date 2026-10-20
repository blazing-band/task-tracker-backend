import logging
from dataclasses import asdict, dataclass

from sqlalchemy import exists, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.user import user_table
from backend.entities import User
from backend.exceptions import NotFound

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class NewUserData:
    username: str
    password: str
    email: str


@dataclass(frozen=True, slots=True)
class UserRepository:
    session: AsyncSession

    async def get_by_id(self, user_id: int) -> User:
        try:
            query = select(User).where(user_table.c.id == user_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound as e:
            raise NotFound("User not found") from e

    async def get_by_email(self, user_email: str) -> User:
        try:
            query = select(User).where(user_table.c.email == user_email)
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound as e:
            raise NotFound("User not found") from e

    async def add(self, user_data: NewUserData) -> User:
        query = insert(User).returning(User)
        result = await self.session.execute(query, asdict(user_data))
        return result.scalar_one()

    async def is_exists(self, user_email: str) -> bool:
        query = select(exists().where(user_table.c.email == user_email))
        result = await self.session.execute(query)
        return result.scalar_one()
