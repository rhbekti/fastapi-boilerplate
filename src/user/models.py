from typing import Optional
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field
from uuid import uuid4


class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(default=None, min_length=1, max_length=255)
    username: str = Field(unique=True, index=True, min_length=1, max_length=255)
    password: str = Field(default=None, min_length=1, max_length=255)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))


class CreateUserRequest(SQLModel):
    name: str = Field(default=None, min_length=1, max_length=255)
    username: str = Field(default=None, min_length=1, max_length=255)
    password: str = Field(default=None, min_length=1, max_length=255)


class UpdateUserRequest(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    username: Optional[str] = Field(default=None, min_length=1, max_length=255)
    password: Optional[str] = Field(default=None, min_length=1, max_length=255)


class UserResponse(SQLModel):
    id: str
    name: str
    username: str
    created_at: datetime
    updated_at: datetime
