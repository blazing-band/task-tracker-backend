from dataclasses import dataclass

from fastapi import Request

from backend.dtos import TaskDto
from backend.repositories import TaskRepository
from backend.services import IdentityProvider, TransactionManager


@dataclass(frozen=True, slots=True)
class EditTaskInput:
    task_id: int
    task_name: str
    task_text: str


@dataclass(frozen=True, slots=True, kw_only=True)
class EditTask:
    task_repository: TaskRepository
    transaction_manager: TransactionManager
    identity_provider: IdentityProvider
    request: Request

    async def __call__(self, task_changes: EditTaskInput) -> TaskDto:
        user = await self.identity_provider.get_user(self.request)
        async with self.transaction_manager:
            task = await self.task_repository.get(task_id=task_changes.task_id, user_id=user.id)
            task.name = task_changes.task_name
            task.text = task_changes.task_text
            return TaskDto(
                id=task.id,
                name=task.name,
                text=task.text,
                status=task.status,
                timestamp=task.timestamp,
            )
