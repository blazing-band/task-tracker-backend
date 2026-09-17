import logging
from dataclasses import dataclass, asdict

from sqlalchemy import select, exists, insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

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
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound:
            raise NotFound(f"User not found")

    async def get_by_email(self, user_email: str) -> User:
        try:
            query = select(User).where(User.email == user_email)
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound:
            raise NotFound(f"User not found")

    async def add(self, user_data: NewUserData) -> User:
        query = insert(User).returning(User)
        result = await self.session.execute(query, asdict(user_data))
        return result.scalar()

    async def is_exists(self, user_email: str) -> bool:
        query = select(exists().where(User.email == user_email))
        result = await self.session.scalar(query)
        return result
