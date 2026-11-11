from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.orm import Session

from backend.database.models.outbox import outbox_table
from backend.entities import Outbox, EventStatus


@dataclass(frozen=True, slots=True)
class SyncOutboxRepository:
    """Sync outbox repository"""

    session: Session

    def get_batch(self) -> list[Outbox]:
        query = select(Outbox).where(outbox_table.c.status == EventStatus.NEW).limit(100).with_for_update(skip_locked=True)
        batch = self.session.execute(query)
        return list(batch.scalars().all())

    def change_status(self, event_uuid: UUID, status: EventStatus) -> None:
        query = update(Outbox).where(outbox_table.c.id == event_uuid).values(status=status)
        self.session.execute(query)
