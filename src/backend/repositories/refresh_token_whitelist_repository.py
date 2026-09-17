from dataclasses import dataclass
from datetime import timedelta

from redis.asyncio import Redis

from backend.settings import Settings


@dataclass(frozen=True, slots=True)
class RefreshTokenWhitelistRepository:

    redis: Redis
    settings: Settings

    async def add(self, refresh_jti: str) -> None:
        """
        Add refresh token to whitelist
        :param refresh_jti:
        :return:
        """
        await self.redis.set(name=f"refresh:{refresh_jti}", value=refresh_jti, ex=timedelta(minutes=self.settings.jwt.refresh_expires_minutes))

    async def remove(self, refresh_jti: str) -> None:
        """
        Remove refresh token from whitelist
        :param refresh_jti:
        :return:
        """
        await self.redis.delete(f"refresh:{refresh_jti}")

    async def is_contains(self, refresh_jti: str) -> bool:
        """
        Check is token in whitelist
        :return:
        """
        result = await self.redis.get(name=f"refresh:{refresh_jti}")
        if result == refresh_jti:
            return True
        return False
