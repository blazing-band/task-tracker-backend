from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, Response, status

from backend.interactors import CreateUser, CreateUserInput, CreateUserOutput
from backend.routers.identity_provider import IdentityProvider

from .schemas import GetUserResponse, PostUserRequest


def get_user_router() -> APIRouter:

    user_router = APIRouter(prefix="/user")

    @user_router.post("")
    @inject
    async def post_user(
        user_credentials: PostUserRequest,
        interactor: FromDishka[CreateUser],
        response: Response,
    ) -> Response:
        result: CreateUserOutput = await interactor(CreateUserInput(**user_credentials.model_dump()))
        response.set_cookie(key="access_token", value=result.access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True)
        response.status_code = status.HTTP_201_CREATED
        return response

    @user_router.get("")
    @inject
    async def get_user(
        identity_provider: FromDishka[IdentityProvider],
        request: Request,
    ) -> GetUserResponse:
        user = await identity_provider.get_user(request)
        return GetUserResponse(id=user.id, username=user.username, email=user.email)

    return user_router
