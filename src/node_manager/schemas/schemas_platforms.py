from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class PlatformBase(BaseModel):
    name: str
    description: str
    type: str


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
