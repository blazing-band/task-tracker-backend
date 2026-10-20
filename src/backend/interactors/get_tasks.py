from dataclasses import dataclass

from backend.dtos import TaskDto
from backend.repositories import TaskRepository


@dataclass(frozen=True, slots=True)
class GetTasksInput:
    user_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTasks:
    task_repository: TaskRepository

    async def __call__(self, interactor_input: GetTasksInput) -> list[TaskDto]:
        tasks = await self.task_repository.get_user_tasks(interactor_input.user_id)
        return [TaskDto(**task.to_dict()) for task in tasks]
