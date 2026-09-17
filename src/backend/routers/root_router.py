from fastapi import APIRouter

from .user import get_user_router
from .session import get_session_router
# from .tasks import get_tasks_router


def get_root_router() -> APIRouter:
    root_router = APIRouter(prefix="/api")

    sub_routers: tuple[APIRouter, ...] = (
        get_user_router(),
        get_session_router(),
        # get_tasks_router()
    )

    for router in sub_routers:
        root_router.include_router(router)

    return root_router
