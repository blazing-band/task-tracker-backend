from pydantic import BaseModel, EmailStr, Field


class PostUserRequest(BaseModel):
    username: str = Field(min_length=6, max_length=120)
    password: str = Field(min_length=6, max_length=64)
    email: EmailStr


class PostUserResponse(BaseModel):
    pass


class GetUserRequest(BaseModel):
    pass


class GetUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
