from dataclasses import dataclass

from backend.repositories import RefreshTokenWhitelistRepository
from backend.services import JwtService


@dataclass(frozen=True, slots=True, kw_only=True)
class Logout:
    jwt_service: JwtService
    refresh_token_whitelist_repository: RefreshTokenWhitelistRepository

    async def __call__(
        self,
        refresh_token: str,
    ) -> None:
        token_payload = self.jwt_service.get_payload(refresh_token)
        await self.refresh_token_whitelist_repository.remove(token_payload["jti"])
