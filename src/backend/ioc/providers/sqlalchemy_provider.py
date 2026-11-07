import logging
from collections.abc import AsyncGenerator, AsyncIterable
from typing import Any

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.settings import Settings

logger = logging.getLogger(__name__)


class SqlAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, settings: Settings) -> AsyncGenerator[AsyncEngine, Any]:
        engine = create_async_engine(url=settings.db.database_url)
        exc = yield engine
        if exc:
            logger.warning("Some exception while engine was used", exc)
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_factory(self, engine: AsyncEngine) -> AsyncIterable[async_sessionmaker[AsyncSession]]:
        session_factory = async_sessionmaker(engine)
        yield session_factory

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
        async with session_factory() as session:
            exc = yield session
            if exc:
                logger.warning("Some exception while session was used", exc)
