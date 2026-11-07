from dataclasses import asdict

import pytest
from fastapi import status
from httpx import AsyncClient

from tests.backend.integration.factories import UserCredentials


class TestUserRouters:
    @pytest.mark.asyncio
    async def test_create_user(self, app_client: AsyncClient, user_credentials: UserCredentials) -> None:
        response = await app_client.post("/api/user", json=asdict(user_credentials))
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        assert "access_token" in response.cookies, "access_token cookie not found"
        assert "refresh_token" in response.cookies, "refresh_token cookie not found"

    @pytest.mark.asyncio
    async def test_get_user(self, authorized_app_client: AsyncClient, user_credentials: UserCredentials) -> None:
        response = await authorized_app_client.get("/api/user")
        assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}: {response.text}"
        response_body = response.json()
        assert response_body["username"] == user_credentials.username
        assert response_body["email"] == user_credentials.email
