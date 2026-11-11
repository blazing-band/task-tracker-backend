import logging
from dataclasses import dataclass

from backend.entities import Outbox, EventType
from backend.repositories import NewUserData, RefreshTokenWhitelistRepository, UserRepository, OutboxRepository
from backend.services import JwtService, PasswordHasher, TransactionManager

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class CreateUserInput:
    username: str
    password: str
    email: str


@dataclass(slots=True, frozen=True)
class CreateUserOutput:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUser:
    transaction_manager: TransactionManager
    user_repository: UserRepository
    outbox_repository: OutboxRepository
    password_hasher: PasswordHasher
    jwt_service: JwtService
    refresh_token_whitelist_repository: RefreshTokenWhitelistRepository

    async def __call__(self, new_user: CreateUserInput) -> CreateUserOutput:
        hashed_pass = self.password_hasher.hash_password(new_user.password)
        async with self.transaction_manager:
            new_user_data = NewUserData(
                username=new_user.username,
                password=hashed_pass,
                email=new_user.email,
            )
            user = await self.user_repository.add(new_user_data)
            outbox = Outbox(
                event_type=EventType.USER_CREATED,
                payload={
                    "email": user.email
                },
            )
            await self.outbox_repository.add(outbox)
            access_token = self.jwt_service.create_access_token(user=user)
            refresh_token = self.jwt_service.create_refresh_token(user=user)
            refresh_jti = self.jwt_service.get_payload(refresh_token)["jti"]
            await self.refresh_token_whitelist_repository.add(refresh_jti)

        return CreateUserOutput(access_token=access_token, refresh_token=refresh_token)
