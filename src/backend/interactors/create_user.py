import logging
from dataclasses import dataclass

from backend.repositories import NewUserData, RefreshTokenWhitelistRepository, UserRepository
from backend.services import EmailProducer, JwtService, PasswordHasher, TransactionManager

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
    password_hasher: PasswordHasher
    jwt_service: JwtService
    refresh_token_whitelist_repository: RefreshTokenWhitelistRepository
    email_producer: EmailProducer

    async def __call__(self, new_user: CreateUserInput) -> CreateUserOutput:
        hashed_pass = self.password_hasher.hash_password(new_user.password)
        async with self.transaction_manager:
            new_user_data = NewUserData(
                username=new_user.username,
                password=hashed_pass,
                email=new_user.email,
            )
            user = await self.user_repository.add(new_user_data)
            access_token = self.jwt_service.create_access_token(user=user)
            refresh_token = self.jwt_service.create_refresh_token(user=user)
            refresh_jti = self.jwt_service.get_payload(refresh_token)["jti"]
            await self.refresh_token_whitelist_repository.add(refresh_jti)

        # Publish only after commit so no email goes out for a rolled-back user.
        # `user` is expired after commit, so use the input email instead of lazy-loading it.
        # The welcome email is not critical: a broker outage must not fail registration.
        try:
            self.email_producer.send_user_registration_email(email=new_user.email)
        except Exception:
            logger.exception("Failed to publish registration email task for %s", new_user.email)

        return CreateUserOutput(access_token=access_token, refresh_token=refresh_token)
