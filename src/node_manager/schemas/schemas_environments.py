from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from node_manager.schemas.schemas_nodes import NodeRead


class EnvironmentBase(BaseModel):
    name: str
    description: str


class EnvironmentCreate(EnvironmentBase):
    pass


class EnvironmentDetailsRead(EnvironmentBase):
    id: int
    created_at: datetime
    platform_id: int
    nodes: List[NodeRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class PlatformEnvironmentRead(EnvironmentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
