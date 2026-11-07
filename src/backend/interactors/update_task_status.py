from dataclasses import dataclass

from fastapi import Request

from backend.dtos import TaskDto
from backend.exceptions import NotFoundError
from backend.repositories import TaskRepository
from backend.services import IdentityProvider, TransactionManager


@dataclass(frozen=True, slots=True)
class UpdateTaskStatusInput:
    task_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateTaskStatus:
    task_repository: TaskRepository
    transaction_manager: TransactionManager
    identity_provider: IdentityProvider
    request: Request

    async def __call__(self, task_ref: UpdateTaskStatusInput) -> TaskDto:
        user = await self.identity_provider.get_user(self.request)
        async with self.transaction_manager:
            if not await self.task_repository.is_exists(task_id=task_ref.task_id, user_id=user.id):
                raise NotFoundError("Task not founded")
            task = await self.task_repository.change_status(task_id=task_ref.task_id, user_id=user.id)
            return TaskDto(
                id=task.id,
                name=task.name,
                text=task.text,
                status=task.status,
                timestamp=task.timestamp,
            )
