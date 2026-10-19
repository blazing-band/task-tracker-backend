from dataclasses import dataclass

from backend.exceptions import InvalidPassword
from backend.repositories import RefreshTokenWhitelistRepository, UserRepository
from backend.services import JwtService, PasswordHasher, TransactionManager


@dataclass(slots=True, frozen=True)
class CreateSessionInput:
    password: str
    email: str


@dataclass(slots=True, frozen=True)
class CreateSessionOutput:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateSession:
    transaction_manager: TransactionManager
    user_repository: UserRepository
    password_hasher: PasswordHasher
    jwt_service: JwtService
    refresh_token_whitelist_repository: RefreshTokenWhitelistRepository

    async def __call__(
        self,
        interactor_input: CreateSessionInput,
    ) -> CreateSessionOutput:
        async with self.transaction_manager:
            user = await self.user_repository.get_by_email(interactor_input.email)
            if not self.password_hasher.compare(user.password, interactor_input.password):
                raise InvalidPassword("Password mismatch")
            access_token = self.jwt_service.create_access_token(user=user)
            refresh_token = self.jwt_service.create_refresh_token(user=user)
            await self.refresh_token_whitelist_repository.add(refresh_token)
            return CreateSessionOutput(access_token=access_token, refresh_token=refresh_token)
