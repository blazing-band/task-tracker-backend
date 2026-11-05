from dishka import Provider, Scope, provide

from backend.interactors import (
    CreateSession,
    CreateTask,
    CreateUser,
    DeleteTask,
    EditTask,
    Logout,
    RefreshTokens,
    UpdateTaskStatus,
)
from backend.interactors.get_tasks import GetTasks


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser)
    create_session = provide(CreateSession)
    logout = provide(Logout)
    refresh_tokens = provide(RefreshTokens)
    get_tasks = provide(GetTasks)
    create_task = provide(CreateTask)
    delete_task = provide(DeleteTask)
    update_task_status = provide(UpdateTaskStatus)
    edit_task = provide(EditTask)
