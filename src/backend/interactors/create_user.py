from dataclasses import dataclass

from backend.exceptions import AlreadyExists
from backend.repositories import UserRepository, NewUserData
from backend.services import JwtService, PasswordHasher, TransactionManager

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

    async def __call__(
        self,
        interactor_input: CreateUserInput
    ) -> CreateUserOutput:
        async with self.transaction_manager:
            if await self.user_repository.is_exists(interactor_input.email):
                raise AlreadyExists("User already exists")
            hashed_pass = self.password_hasher.hash_password(interactor_input.password)
            new_user_data = NewUserData(
                username=interactor_input.username,
                password=hashed_pass,
                email=interactor_input.email
            )
            user = await self.user_repository.add(new_user_data)
            access_token = self.jwt_service.create_access_token(
                user=user
            )
            refresh_token = self.jwt_service.create_refresh_token(user=user)
            # TODO send message to user email
            return CreateUserOutput(access_token=access_token, refresh_token=refresh_token)
