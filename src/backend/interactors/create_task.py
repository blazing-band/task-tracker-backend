from dataclasses import dataclass

from fastapi import Request

from backend.dtos import TaskDto
from backend.repositories import NewTaskData, TaskRepository
from backend.services import IdentityProvider, TransactionManager


@dataclass(frozen=True, slots=True)
class CreateTaskInput:
    task_name: str
    task_text: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTask:
    task_repository: TaskRepository
    transaction_manager: TransactionManager
    identity_provider: IdentityProvider
    request: Request

    async def __call__(self, new_task: CreateTaskInput) -> TaskDto:
        user = await self.identity_provider.get_user(self.request)
        new_task_data = NewTaskData(
            user_id=user.id,
            name=new_task.task_name,
            text=new_task.task_text,
        )
        async with self.transaction_manager:
            task = await self.task_repository.add(new_task_data)
            return TaskDto(
                id=task.id,
                name=task.name,
                text=task.text,
                status=task.status,
                timestamp=task.timestamp,
            )
