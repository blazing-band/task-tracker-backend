from dataclasses import dataclass

from fastapi import Request

from backend.entities import User
from backend.repositories import UserRepository
from backend.services import JwtService


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentityProvider:
    """
    Check jwt token from request and return User
    """

    user_repository: UserRepository
    jwt_service: JwtService

    async def get_user(self, request: Request) -> User:
        access_token = request.cookies.get("access_token")
        token_payload = self.jwt_service.get_payload(access_token)
        user_id = int(token_payload["sub"])
        user = await self.user_repository.get_by_id(user_id)
        return user
