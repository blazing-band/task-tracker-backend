from dishka import Provider, provide, Scope
from redis.asyncio import Redis

from backend.settings import Settings


class RedisProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_redis(
        self,
        settings: Settings,
    ) -> Redis:
        return Redis(
            host=settings.redis.redis_host,
            port=settings.redis.redis_port,
            password=settings.redis.redis_password
        )
