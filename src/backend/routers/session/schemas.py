from pydantic import BaseModel, EmailStr, Field


class PostSessionRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
