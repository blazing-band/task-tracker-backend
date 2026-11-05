from fastapi import APIRouter

from .session import session_router
from .task import task_router
from .user import user_router


def get_root_router() -> APIRouter:
    root_router = APIRouter(prefix="/api")

    sub_routers: tuple[APIRouter, ...] = (user_router, session_router, task_router)

    for router in sub_routers:
        root_router.include_router(router)

    return root_router
