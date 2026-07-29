from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: str
    name: str
    username: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateUserRequest(BaseModel):
    name: str
    username: str
    email: Optional[str] = None


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
