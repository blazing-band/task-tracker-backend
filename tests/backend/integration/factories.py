from dataclasses import dataclass

import factory


@dataclass(slots=True, frozen=True)
class UserCredentials:
    username: str
    password: str
    email: str


class UserCredentialsFactory(factory.Factory[UserCredentials]):
    class Meta:
        model = UserCredentials

    username = factory.Sequence(lambda n: f"user_{n}")
    password = "test_password"
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
