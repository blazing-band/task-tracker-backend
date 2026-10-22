import asyncio
import os
import sys
from collections.abc import AsyncIterator, Iterator
from dataclasses import asdict

import pytest
import pytest_asyncio
from alembic.config import Config
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer

from alembic import command
from backend.app import create_app
from tests.backend.integration.factories import UserCredentials, UserCredentialsFactory

load_dotenv()

# Windows: psycopg3 doesn't work with ProactorEventLoop (default on Windows)
# Set WindowsSelectorEventLoopPolicy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def postgres() -> Iterator[PostgresContainer]:
    with PostgresContainer("postgres:18.4") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def redis() -> Iterator[RedisContainer]:
    with RedisContainer("redis:8.10.0") as redis:
        yield redis


@pytest.fixture(scope="session", autouse=True)
def setup(postgres: PostgresContainer, redis: RedisContainer) -> None:
    os.environ["DB_DRIVER"] = "postgresql+psycopg"
    os.environ["DB_NAME"] = postgres.dbname
    os.environ["DB_USER"] = postgres.username
    os.environ["DB_PASS"] = postgres.password
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))

    os.environ["REDIS_HOST"] = redis.get_container_host_ip()
    os.environ["REDIS_PASSWORD"] = str(redis.password) if redis.password else ""
    os.environ["REDIS_PORT"] = str(redis.get_exposed_port(redis.port))

    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["JWT_SECRET"] = "okS7XXCoWD8bDgNkmvbgB6pXgIPIrO0dJygE6MvcLH0"
    os.environ["JWT_ACCESS_EXPIRATION_MINUTES"] = "15"
    os.environ["JWT_REFRESH_EXPIRATION_MINUTES"] = "60"

    os.environ["CORS_ORIGINS"] = "http://localhost:3000"

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest_asyncio.fixture
async def app_client(setup: None) -> AsyncIterator[AsyncClient]:
    """
    Create a fresh AsyncClient for each test, so cookies don't leak between tests.
    :param setup:
    :return:
    """
    async with AsyncClient(transport=ASGITransport(create_app()), base_url="http://test") as client:
        yield client


@pytest.fixture
def user_credentials() -> UserCredentials:
    credentials: UserCredentials = UserCredentialsFactory.build()
    return credentials


@pytest_asyncio.fixture
async def authorized_app_client(app_client: AsyncClient, user_credentials: UserCredentials) -> AsyncClient:
    """
    Register a new user and return client authorized as him
    :param app_client:
    :param user_credentials:
    :return:
    """
    response = await app_client.post("/api/user", json=asdict(user_credentials))
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"

    access_token = response.cookies.get("access_token")
    refresh_token = response.cookies.get("refresh_token")
    assert access_token is not None, "access_token cookie не найден"
    assert refresh_token is not None, "refresh_token cookie не найден"

    app_client.cookies.set("access_token", access_token)
    app_client.cookies.set("refresh_token", refresh_token)

    return app_client
