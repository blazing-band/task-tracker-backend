from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt

from backend.entities import User
from backend.settings import Settings


class JwtService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_access_token(self, user: User) -> str:
        iat = datetime.now(UTC)
        jwt_payload = {
            "jti": str(uuid4()),
            "sub": str(user.id),
            "type": "access",
            "iat": iat,
            "exp": iat + timedelta(minutes=self.settings.jwt.access_expires_minutes),
        }
        jwt_token = jwt.encode(
            jwt_payload,
            self.settings.jwt.jwt_secret,
            algorithm=self.settings.jwt.jwt_algorithm,
        )
        return jwt_token

    def create_refresh_token(self, user: User) -> str:
        iat = datetime.now(UTC)
        jwt_payload = {
            "jti": str(uuid4()),
            "sub": str(user.id),
            "type": "refresh",
            "iat": iat,
            "exp": iat + timedelta(minutes=self.settings.jwt.refresh_expires_minutes),
        }
        jwt_token = jwt.encode(
            jwt_payload,
            self.settings.jwt.jwt_secret,
            algorithm=self.settings.jwt.jwt_algorithm,
        )
        return jwt_token

    def get_payload(self, token: str) -> dict:
        """
        Decode jwt token and return token payload
        :param token:
        :return:
        """
        payload = jwt.decode(
            token,
            self.settings.jwt.jwt_secret,
            algorithms=[self.settings.jwt.jwt_algorithm],
        )
        return payload
