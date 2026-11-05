from dataclasses import dataclass

from backend.exceptions import NotFoundError
from backend.repositories import TaskRepository
from backend.services import TransactionManager


@dataclass(frozen=True, slots=True)
class DeleteTaskInput:
    user_id: int
    task_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTask:
    task_repository: TaskRepository
    transaction_manager: TransactionManager

    async def __call__(self, interactor_input: DeleteTaskInput) -> None:
        async with self.transaction_manager:
            await self.task_repository.delete(task_id=interactor_input.task_id)
