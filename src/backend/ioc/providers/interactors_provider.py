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
    create_user = provide(CreateUser, scope=Scope.REQUEST)
    create_session = provide(CreateSession, scope=Scope.REQUEST)
    logout = provide(Logout, scope=Scope.REQUEST)
    refresh_tokens = provide(RefreshTokens, scope=Scope.REQUEST)
    get_tasks = provide(GetTasks, scope=Scope.REQUEST)
    create_task = provide(CreateTask, scope=Scope.REQUEST)
    delete_task = provide(DeleteTask, scope=Scope.REQUEST)
    update_task_status = provide(UpdateTaskStatus, scope=Scope.REQUEST)
    edit_task = provide(EditTask, scope=Scope.REQUEST)
