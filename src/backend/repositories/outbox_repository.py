from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities import Outbox


@dataclass(frozen=True, slots=True)
class OutboxRepository:

    session: AsyncSession

    async def add(self, outbox: Outbox) -> None:
        self.session.add(outbox)
