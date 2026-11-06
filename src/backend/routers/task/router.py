from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, Response, status

from backend.dtos import TaskDto
from backend.interactors import (
    DeleteTask,
    DeleteTaskInput,
    EditTask,
    EditTaskInput,
    UpdateTaskStatus,
    UpdateTaskStatusInput,
)
from backend.interactors.create_task import CreateTask, CreateTaskInput
from backend.interactors.get_tasks import GetTasks
from backend.routers.task.schemas import (
    CreateTaskRequest,
    UpdateTaskTextRequest,
)

task_router = APIRouter(prefix="/tasks")


@task_router.get("")
@inject
async def get_tasks(
    interactor: FromDishka[GetTasks],
) -> list[TaskDto]:
    """
    Get all tasks
    :return:
    """
    result = await interactor()
    return result


@task_router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_task(
    task_data: CreateTaskRequest,
    interactor: FromDishka[CreateTask],
) -> TaskDto:
    """
    Create a new task
    :param task_data:
    :param interactor:
    :return:
    """
    result = await interactor(CreateTaskInput(task_name=task_data.name, task_text=task_data.text))
    return result


@task_router.patch("")
@inject
async def update_task_status(
    task_id: Annotated[int, Query(alias="taskId")],
    interactor: FromDishka[UpdateTaskStatus],
) -> TaskDto:
    """
    Update task status
    :param task_id:
    :param interactor:
    :return:
    """
    task = await interactor(UpdateTaskStatusInput(task_id=task_id))
    return task


@task_router.patch("/edit")
@inject
async def update_task_text(
    task_id: Annotated[int, Query(alias="taskId")],
    task_data: UpdateTaskTextRequest,
    interactor: FromDishka[EditTask],
) -> TaskDto:
    """
    Edit task name and text
    :param task_id:
    :param task_data:
    :param interactor:
    :return:
    """
    task = await interactor(EditTaskInput(task_id=task_id, task_name=task_data.name, task_text=task_data.text))
    return task


@task_router.delete("")
@inject
async def delete_task(
    task_id: Annotated[int, Query(alias="taskId")],
    interactor: FromDishka[DeleteTask],
) -> Response:
    """
    Delete task
    :param task_id:
    :param interactor:
    :return:
    """
    await interactor(DeleteTaskInput(task_id=task_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
