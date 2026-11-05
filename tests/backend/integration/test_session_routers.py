import pytest
from fastapi import status
from httpx import AsyncClient

from tests.backend.integration.factories import UserCredentials


def get_refresh_token(client: AsyncClient) -> str:
    """
    Return refresh token from client cookies
    :param client:
    :return:
    """
    return next(cookie.value for cookie in client.cookies.jar if cookie.name == "refresh_token" and cookie.value)


def use_refresh_token(client: AsyncClient, refresh_token: str) -> None:
    """
    Replace all client cookies with the given refresh token.
    httpx stores response cookies itself, so plain cookies.set would create a duplicate.
    :param client:
    :param refresh_token:
    :return:
    """
    client.cookies.clear()
    client.cookies.set("refresh_token", refresh_token)


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

    @pytest.mark.asyncio
    async def test_refresh_twice(self, authorized_app_client: AsyncClient) -> None:
        response = await authorized_app_client.get("/api/session/refresh")
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        use_refresh_token(authorized_app_client, response.cookies["refresh_token"])

        response = await authorized_app_client.get("/api/session/refresh")
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )

    @pytest.mark.asyncio
    async def test_refresh_with_used_token(self, authorized_app_client: AsyncClient) -> None:
        old_refresh_token = get_refresh_token(authorized_app_client)
        response = await authorized_app_client.get("/api/session/refresh")
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )

        use_refresh_token(authorized_app_client, old_refresh_token)
        response = await authorized_app_client.get("/api/session/refresh")
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            f"Expected 404, got {response.status_code}: {response.text}"
        )

    @pytest.mark.asyncio
    async def test_refresh_after_logout(self, authorized_app_client: AsyncClient) -> None:
        response = await authorized_app_client.delete("/api/session")
        assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}: {response.text}"

        response = await authorized_app_client.get("/api/session/refresh")
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            f"Expected 404, got {response.status_code}: {response.text}"
        )
