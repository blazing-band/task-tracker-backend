from datetime import datetime

from pydantic import BaseModel

from backend.entities import TaskStatus


class GetTasksResponse(BaseModel):
    id: int
    name: str
    text: str
    status: TaskStatus
    timestamp: datetime


class CreateTaskRequest(BaseModel):
    name: str
    text: str


class CreateTaskResponse(BaseModel):
    id: int
    name: str
    text: str
    status: TaskStatus
    timestamp: datetime


class UpdateTaskStatusResponse(BaseModel):
    id: int
    name: str
    text: str
    status: TaskStatus
    timestamp: datetime


class UpdateTaskTextRequest(BaseModel):
    name: str
    text: str


class UpdateTaskTextResponse(BaseModel):
    id: int
    name: str
    text: str
    status: TaskStatus
    timestamp: datetime
