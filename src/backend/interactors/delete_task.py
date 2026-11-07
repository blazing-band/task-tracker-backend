from dataclasses import dataclass

from fastapi import Request

from backend.repositories import TaskRepository
from backend.services import IdentityProvider, TransactionManager


@dataclass(frozen=True, slots=True)
class DeleteTaskInput:
    task_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTask:
    task_repository: TaskRepository
    transaction_manager: TransactionManager
    identity_provider: IdentityProvider
    request: Request

    async def __call__(self, task_ref: DeleteTaskInput) -> None:
        user = await self.identity_provider.get_user(self.request)
        async with self.transaction_manager:
            await self.task_repository.delete(task_id=task_ref.task_id, user_id=user.id)
