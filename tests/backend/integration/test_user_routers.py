import pytest
from fastapi import status
from httpx import AsyncClient


class TestUserRouters:

    @pytest.mark.asyncio
    async def test_get_user(
        self,
        authorized_app_client: AsyncClient,
        user_credentials: dict[str, str],
    ) -> None:
        response = await authorized_app_client.get("/api/user")
        assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}: {response.text}"

        response_body = response.json()
        assert response_body["username"] == user_credentials["username"]
        assert response_body["email"] == user_credentials["email"]
