from dataclasses import dataclass

from fastapi import Request

from backend.dtos import TaskDto
from backend.repositories import TaskRepository
from backend.services import IdentityProvider


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTasks:
    task_repository: TaskRepository
    identity_provider: IdentityProvider
    request: Request

    async def __call__(self) -> list[TaskDto]:
        user = await self.identity_provider.get_user(self.request)
        tasks = await self.task_repository.get_user_tasks(user.id)
        return [
            TaskDto(
                id=task.id,
                name=task.name,
                text=task.text,
                status=task.status,
                timestamp=task.timestamp,
            )
            for task in tasks
        ]
