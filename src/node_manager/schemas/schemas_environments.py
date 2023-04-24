from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class EnvironmentBase(BaseModel):
    name: str
    description: str


class EnvironmentCreate(EnvironmentBase):
    pass


class EnvironmentRead(EnvironmentBase):
    id: UUID
    created_at: datetime
    platform_id: UUID

    class Config:
        orm_mode = True
