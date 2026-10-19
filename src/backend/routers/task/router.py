from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Response

from .schemas import (
    CreateTaskRequest,
    CreateTaskResponse,
    GetTasksResponse,
    UpdateTaskStatusResponse,
    UpdateTaskTextRequest,
    UpdateTaskTextResponse,
)


def get_task_router() -> APIRouter:

    task_router = APIRouter(prefix="/tasks")

    @task_router.get("")
    @inject
    async def get_tasks() -> list[GetTasksResponse]:
        """
        Get all tasks
        :return:
        """

    @task_router.post("")
    @inject
    async def create_task(task: CreateTaskRequest) -> CreateTaskResponse:
        """
        Create a new task
        :param task:
        :return:
        """

    @task_router.patch("")
    @inject
    async def update_task_status(task_id: str) -> UpdateTaskStatusResponse:
        """
        Update task status
        :param task_id:
        :return:
        """

    @task_router.patch("/edit")
    @inject
    async def update_task_text(task_id: str, data: UpdateTaskTextRequest) -> UpdateTaskTextResponse:
        """
        Update task text
        :param task_id:
        :param data:
        :return:
        """

    @task_router.delete("")
    @inject
    async def delete_task(task_id: int) -> Response:
        """
        Delete task
        :param task_id:
        :return:
        """

    return task_router
