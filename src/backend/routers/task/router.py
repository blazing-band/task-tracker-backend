from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, Request, Response, status

from backend.interactors.get_tasks import GetTasks, GetTasksInput
from backend.routers.identity_provider import IdentityProvider

from ...dtos import TaskDto
from ...interactors import DeleteTask, DeleteTaskInput, EditTask, EditTaskInput, UpdateTaskStatus, UpdateTaskStatusInput
from ...interactors.create_task import CreateTask, CreateTaskInput
from .schemas import (
    CreateTaskRequest,
    UpdateTaskTextRequest,
)


def get_task_router() -> APIRouter:

    task_router = APIRouter(prefix="/tasks")

    @task_router.get("")
    @inject
    async def get_tasks(
        request: Request,
        interactor: FromDishka[GetTasks],
        identity_provider: FromDishka[IdentityProvider],
    ) -> list[TaskDto]:
        """
        Get all tasks
        :return:
        """
        user = await identity_provider.get_user(request)
        result = await interactor(GetTasksInput(user_id=user.id))
        return result

    @task_router.post("")
    @inject
    async def create_task(
        request: Request,
        task_data: CreateTaskRequest,
        interactor: FromDishka[CreateTask],
        identity_provider: FromDishka[IdentityProvider],
    ) -> TaskDto:
        """
        Create a new task
        :param request:
        :param task_data:
        :param interactor:
        :param identity_provider:
        :return:
        """
        user = await identity_provider.get_user(request)
        result = await interactor(CreateTaskInput(user_id=user.id, task_name=task_data.name, task_text=task_data.text))
        return result

    @task_router.patch("")
    @inject
    async def update_task_status(
        request: Request,
        task_id: Annotated[int, Query(alias="taskId")],
        interactor: FromDishka[UpdateTaskStatus],
        identity_provider: FromDishka[IdentityProvider],
    ) -> TaskDto:
        """
        Update task status
        :param request:
        :param task_id:
        :param interactor:
        :param identity_provider:
        :return:
        """
        user = await identity_provider.get_user(request)
        task = await interactor(UpdateTaskStatusInput(task_id=task_id, user_id=user.id))
        return task

    @task_router.patch("/edit")
    @inject
    async def update_task_text(
        task_id: Annotated[int, Query(alias="taskId")],
        task_data: UpdateTaskTextRequest,
        request: Request,
        interactor: FromDishka[EditTask],
        identity_provider: FromDishka[IdentityProvider],
    ) -> TaskDto:
        """
        Edit task name and text
        :param task_id:
        :param task_data:
        :param request:
        :param interactor:
        :param identity_provider:
        :return:
        """
        user = await identity_provider.get_user(request)
        task = await interactor(
            EditTaskInput(task_id=task_id, user_id=user.id, task_name=task_data.name, task_text=task_data.text)
        )
        return task

    @task_router.delete("")
    @inject
    async def delete_task(
        request: Request,
        task_id: Annotated[int, Query(alias="taskId")],
        interactor: FromDishka[DeleteTask],
        identity_provider: FromDishka[IdentityProvider],
    ) -> Response:
        """
        Delete task
        :param request:
        :param task_id:
        :param interactor:
        :param identity_provider:
        :return:
        """
        user = await identity_provider.get_user(request)
        await interactor(DeleteTaskInput(task_id=task_id, user_id=user.id))
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return task_router
