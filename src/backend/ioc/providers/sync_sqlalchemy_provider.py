import logging
from collections.abc import Iterator

from dishka import Provider, Scope, provide
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.settings import Settings

logger = logging.getLogger(__name__)


class SyncSqlAlchemyProvider(Provider):
    """Sync SQLAlchemy for Celery: tasks run synchronously, so no event loop is needed."""

    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> Iterator[Engine]:
        engine = create_engine(url=settings.db.database_url)
        yield engine
        engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: Engine) -> sessionmaker[Session]:
        return sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    def get_session(self, session_factory: sessionmaker[Session]) -> Iterator[Session]:
        with session_factory() as session:
            exc = yield session
            if exc:
                logger.warning("Some exception while session was used: %s", exc)
