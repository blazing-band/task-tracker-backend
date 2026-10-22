import pytest
from fastapi import status
from httpx import AsyncClient


class TestTaskRouters:
    @pytest.mark.asyncio
    async def test_create_task(self, authorized_app_client: AsyncClient) -> None:
        task_data = {"name": "Test Task", "text": "Test task text"}
        response = await authorized_app_client.post("/api/tasks", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        response_body = response.json()
        assert response_body["name"] == task_data["name"]
        assert response_body["text"] == task_data["text"]
        assert response_body["status"] == "IN_PROGRESS"
        assert "id" in response_body
        assert "timestamp" in response_body

    @pytest.mark.asyncio
    async def test_get_tasks(self, authorized_app_client: AsyncClient) -> None:
        response = await authorized_app_client.get("/api/tasks")
        assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}: {response.text}"
        response_body = response.json()
        assert isinstance(response_body, list)
        if response_body:
            task = response_body[0]
            assert "id" in task
            assert "name" in task
            assert "text" in task
            assert "status" in task
            assert "timestamp" in task

    @pytest.mark.asyncio
    async def test_update_task_status(self, authorized_app_client: AsyncClient) -> None:
        task_data = {"name": "Status Task", "text": "Task for status update"}
        response = await authorized_app_client.post("/api/tasks", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        task_id = response.json()["id"]

        response = await authorized_app_client.patch(f"/api/tasks?taskId={task_id}")
        assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}: {response.text}"
        response_body = response.json()
        assert response_body["status"] == "DONE"

    @pytest.mark.asyncio
    async def test_edit_task(self, authorized_app_client: AsyncClient) -> None:
        task_data = {"name": "Edit Task", "text": "Original text"}
        response = await authorized_app_client.post("/api/tasks", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        task_id = response.json()["id"]

        edit_data = {"name": "Edited Task", "text": "Updated text"}
        response = await authorized_app_client.patch(f"/api/tasks/edit?taskId={task_id}", json=edit_data)
        assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}: {response.text}"
        response_body = response.json()
        assert response_body["name"] == edit_data["name"]
        assert response_body["text"] == edit_data["text"]

    @pytest.mark.asyncio
    async def test_delete_task(self, authorized_app_client: AsyncClient) -> None:

        task_data = {"name": "Delete Task", "text": "Task to delete"}
        response = await authorized_app_client.post("/api/tasks", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        task_id = response.json()["id"]

        response = await authorized_app_client.delete(f"/api/tasks?taskId={task_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f"Expected 204, got {response.status_code}: {response.text}"
        )
