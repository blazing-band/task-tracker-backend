from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from backend.routers import get_root_router, exception_handler
from backend.database import map_tables
from backend.ioc import get_container
from backend.logger import set_up_logger
from backend.routers.exception_handler import custom_request_validation_error_handler
from backend.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    set_up_logger()
    map_tables()
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:

    app = FastAPI(lifespan=lifespan)

    app.include_router(get_root_router())
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=custom_request_validation_error_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=exception_handler
    )
    container = get_container()

    setup_dishka(container, app)

    settings = container.get_sync(Settings)

    app.add_middleware(
        CORSMiddleware,
        settings.app.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

def main() -> None:
    uvicorn.run(
        app="backend.app:create_app",
        factory=True,
        port=8080,
        reload=True
    )


if __name__ == "__main__":
    main()
