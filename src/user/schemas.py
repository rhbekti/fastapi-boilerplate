from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)


class CreateUser(UserBase):
    pass


class UpdateUser(BaseModel):
    name: str | None = Field(min_length=1, max_length=100)
    username: str | None = Field(min_length=3, max_length=100)
    password: str | None = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    created_at: datetime
    updated_at: datetime
