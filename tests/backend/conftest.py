import os

import pytest
from alembic import command
from alembic.config import Config
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer
from fastapi.testclient import TestClient

from backend.app import create_app

@pytest.fixture(scope="session")
def postgres() -> PostgresContainer:
    with PostgresContainer("postgres:18.4", driver="psycopg", dbname="task_tracker_backend") as postgres:
        return postgres

@pytest.fixture(scope="session")
def redis() -> RedisContainer:
    with RedisContainer("redis:8.10.0") as redis:
        return redis

@pytest.fixture(scope="session")
def setup(postgres: PostgresContainer, redis: RedisContainer):
    """
    :param postgres:
    :param redis:
    :return:
    """

    os.environ["DB_DRIVER"] = "postgresql" + postgres.driver
    os.environ["DB_NAME"] = postgres.dbname
    os.environ["DB_USER"] = postgres.username
    os.environ["DB_PASS"] = postgres.password
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] =  str(postgres.port)

    os.environ["REDIS_URL"] = redis.get_container_host_ip()
    os.environ["REDIS_PASSWORD"] = redis.password
    os.environ["REDIS_PORT"] = str(redis.port)

    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["JWT_SECRET"] = "okS7XXCoWD8bDgNkmvbgB6pXgIPIrO0dJygE6MvcLH0"
    os.environ["JWT_ACCESS_EXPIRATION_MINUTES"] = "15"
    os.environ["JWT_REFRESH_EXPIRATION_MINUTES"] = "60"

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(scope="session")
def app_client() -> TestClient:
    """
    Create a test client.
    :return:
    """
    return TestClient(create_app())
