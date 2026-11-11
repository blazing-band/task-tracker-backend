from dataclasses import dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from backend.database.models.task import task_table
from backend.entities import Task, User
from backend.settings import TIMEZONE


@dataclass(frozen=True, slots=True)
class SyncTaskRepository:
    """Sync task repository for Celery tasks."""

    session: Session

    def get_user_tasks_for_previous_day(self, user_id: int) -> list[Task]:
        """
        Return all user's tasks created during the previous (already finished) day.
        The day is taken in TIMEZONE, the same timezone as the beat schedule.
        :param user_id:
        :return:
        """
        today = datetime.now(ZoneInfo(TIMEZONE)).date()
        day_end = datetime.combine(today, time.min)
        day_start = day_end - timedelta(days=1)
        query = select(Task).where(
            and_(
                task_table.c.user_id == user_id,
                task_table.c.timestamp >= day_start,
                task_table.c.timestamp < day_end,
            )
        )
        result = self.session.execute(query)
        return list(result.scalars().all())

    def get_all_users(self) -> list[User]:
        """
        Return all users.
        :return:
        """
        query = select(User)
        result = self.session.execute(query)
        return list(result.scalars().all())
