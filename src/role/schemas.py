from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class CreateRole(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class UpdateRole(BaseModel):
    name: str | None = Field(min_length=1, max_length=255)


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    created_at: datetime
    updated_at: datetime
