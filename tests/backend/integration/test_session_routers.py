import pytest
from fastapi import status
from httpx import AsyncClient

from tests.backend.integration.factories import UserCredentials


class TestSessionRouters:
    @pytest.mark.asyncio
    async def test_login(self, authorized_app_client: AsyncClient, user_credentials: UserCredentials) -> None:
        authorized_app_client.cookies.clear()
        response = await authorized_app_client.post(
            "/api/session",
            json={"email": user_credentials.email, "password": user_credentials.password},
        )
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        assert "access_token" in response.cookies, "access_token cookie not found"
        assert "refresh_token" in response.cookies, "refresh_token cookie not found"

    @pytest.mark.asyncio
    async def test_logout(self, authorized_app_client: AsyncClient) -> None:
        response = await authorized_app_client.delete("/api/session")
        assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}: {response.text}"

    @pytest.mark.asyncio
    async def test_refresh(self, authorized_app_client: AsyncClient) -> None:
        response = await authorized_app_client.get("/api/session/refresh")
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        assert "access_token" in response.cookies, "access_token cookie not found"
        assert "refresh_token" in response.cookies, "refresh_token cookie not found"
