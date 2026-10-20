from dataclasses import asdict, dataclass

from sqlalchemy import and_, case, delete, exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.task import task_table
from backend.entities import Task, TaskStatus


@dataclass(slots=True, frozen=True)
class NewTaskData:
    user_id: int
    name: str
    text: str


@dataclass(frozen=True, slots=True)
class TaskRepository:
    session: AsyncSession

    async def get_user_tasks(self, user_id: int) -> list[Task]:
        """
        Return all users tasks
        :param user_id:
        :return:
        """
        query = select(Task).where(task_table.c.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def add(self, task_data: NewTaskData) -> Task:
        """
        Create new task and return it.
        :param task_data:
        :return:
        """
        query = insert(Task).returning(Task)
        result = await self.session.execute(query, asdict(task_data))
        return result.scalar_one()

    async def delete(self, task_id: int) -> None:
        """
        Delete task
        :param task_id:
        :return:
        """
        query = delete(Task).where(task_table.c.id == task_id)
        await self.session.execute(query)

    async def is_exists(self, task_id: int, user_id: int) -> bool:
        query = select(exists().where(and_(task_table.c.id == task_id, task_table.c.user_id == user_id)))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def change_status(self, task_id: int, user_id: int) -> Task:
        query = (
            update(Task)
            .where(and_(task_table.c.id == task_id, task_table.c.user_id == user_id))
            .values(
                status=case(
                    (task_table.c.status == TaskStatus.DONE, TaskStatus.IN_PROGRESS),
                    else_=TaskStatus.DONE
                )
            )
            .returning(Task)
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def edit(self, task_id: int, user_id: int, task_name: str, task_text: str) -> Task:
        query = update(Task).where(and_(task_table.c.id == task_id, task_table.c.user_id == user_id)).returning(Task)
        result = await self.session.execute(query, {"task_name": task_name, "task_text": task_text})
        return result.scalar_one()
