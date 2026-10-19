from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, Response, status

from backend.interactors import (
    CreateSession,
    CreateSessionInput,
    CreateSessionOutput,
    Logout, RefreshTokens, RefreshTokensInput, RefreshTokensOutput,
)

from .schemas import PostSessionRequest
from ...exceptions import NotFound


def get_session_router() -> APIRouter:

    session_router = APIRouter(prefix="/session")

    @session_router.post("")
    @inject
    async def post_session(
        user_credentials: PostSessionRequest,
        interactor: FromDishka[CreateSession],
        response: Response,
    ) -> Response:
        result: CreateSessionOutput = await interactor(CreateSessionInput(**user_credentials.model_dump()))
        response.set_cookie(key="access_token", value=result.access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True)
        response.status_code = status.HTTP_201_CREATED
        return response

    @session_router.delete("")
    @inject
    async def delete_session(
        interactor: FromDishka[Logout],
        request: Request,
    ) -> Response:
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token is None:
            raise NotFound("Refresh token not found")
        await interactor(refresh_token)
        return Response(content="", status_code=status.HTTP_200_OK)

    @session_router.get("/refresh")
    @inject
    async def refresh_session(
        interactor: FromDishka[RefreshTokens],
        request: Request,
        response: Response,
    ) -> Response:
        """
        Get refresh token and return new access and refresh token.
        :return:
        """
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token is None:
            raise NotFound("Refresh token not found")
        result: RefreshTokensOutput = await interactor(RefreshTokensInput(refresh_token=refresh_token))
        response.set_cookie(key="access_token", value=result.access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True)
        response.status_code = status.HTTP_201_CREATED
        return response

    return session_router
