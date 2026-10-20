from dataclasses import dataclass

from backend.dtos import TaskDto
from backend.repositories import NewTaskData, TaskRepository
from backend.services import TransactionManager


@dataclass(frozen=True, slots=True)
class CreateTaskInput:
    user_id: int
    task_name: str
    task_text: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTask:
    task_repository: TaskRepository
    transaction_manager: TransactionManager

    async def __call__(self, interactor_input: CreateTaskInput) -> TaskDto:
        async with self.transaction_manager:
            new_task_data = NewTaskData(
                user_id=interactor_input.user_id,
                name=interactor_input.task_name,
                text=interactor_input.task_text,
            )
            task = await self.task_repository.add(new_task_data)
            return TaskDto(**task.to_dict())
