from dataclasses import dataclass

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

    async def __call__(
        self,
        interactor_input: RefreshTokensInput
    ) -> RefreshTokensOutput:
        refresh_token_payload = self.jwt_service.get_payload(interactor_input.refresh_token)
        user = await self.user_repository.get_by_id(int(refresh_token_payload["sub"]))
        access_token = self.jwt_service.create_access_token(user=user)
        refresh_token = self.jwt_service.create_refresh_token(user=user)
        return RefreshTokensOutput(access_token=access_token, refresh_token=refresh_token)
