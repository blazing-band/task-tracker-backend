from dataclasses import dataclass

from backend.dtos import TaskDto
from backend.exceptions import NotFound
from backend.repositories import TaskRepository
from backend.services import TransactionManager


@dataclass(frozen=True, slots=True)
class UpdateTaskStatusInput:
    user_id: int
    task_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateTaskStatus:
    task_repository: TaskRepository
    transaction_manager: TransactionManager

    async def __call__(self, interactor_input: UpdateTaskStatusInput) -> TaskDto:
        async with self.transaction_manager:
            if not await self.task_repository.is_exists(
                task_id=interactor_input.task_id, user_id=interactor_input.user_id
            ):
                raise NotFound("Task not founded")
            task = await self.task_repository.change_status(
                task_id=interactor_input.task_id, user_id=interactor_input.user_id
            )
            return TaskDto(**task.to_dict())
