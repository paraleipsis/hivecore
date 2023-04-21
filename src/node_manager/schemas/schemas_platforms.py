from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from node_manager.schemas.schemas_environments import PlatformEnvironmentRead


class PlatformBase(BaseModel):
    name: str
    description: str
    type: str


class PlatformCreate(PlatformBase):
    pass


class PlatformsListRead(PlatformBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PlatformDetailsRead(PlatformBase):
    id: int
    created_at: datetime
    environments: List[PlatformEnvironmentRead] = Field(default_factory=list)

    class Config:
        orm_mode = True
