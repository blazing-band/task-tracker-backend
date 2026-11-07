from dataclasses import dataclass

from backend.exceptions import NotFoundError
from backend.repositories import RefreshTokenWhitelistRepository, UserRepository
from backend.services import JwtService


@dataclass(frozen=True, slots=True)
class RefreshTokensInput:
    refresh_token: str


@dataclass(frozen=True, slots=True)
class RefreshTokensOutput:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshTokens:
    jwt_service: JwtService
    refresh_token_whitelist_repository: RefreshTokenWhitelistRepository
    user_repository: UserRepository

    async def __call__(self, session: RefreshTokensInput) -> RefreshTokensOutput:
        refresh_token_payload = self.jwt_service.get_payload(session.refresh_token)
        old_refresh_jti = refresh_token_payload["jti"]
        if refresh_token_payload["type"] != "refresh":
            raise NotFoundError("Refresh token not found")
        if not await self.refresh_token_whitelist_repository.is_contains(old_refresh_jti):
            raise NotFoundError("Refresh token not found")
        user = await self.user_repository.get_by_id(int(refresh_token_payload["sub"]))
        access_token = self.jwt_service.create_access_token(user=user)
        refresh_token = self.jwt_service.create_refresh_token(user=user)
        await self.refresh_token_whitelist_repository.remove(old_refresh_jti)
        await self.refresh_token_whitelist_repository.add(self.jwt_service.get_payload(refresh_token)["jti"])
        return RefreshTokensOutput(access_token=access_token, refresh_token=refresh_token)
