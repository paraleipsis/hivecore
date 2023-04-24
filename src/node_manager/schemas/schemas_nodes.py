from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class NodeBase(BaseModel):
    name: str
    description: str
    node_ip: str


class NodeCreate(NodeBase):
    pass


class NodeRead(NodeBase):
    id: UUID
    created_at: datetime
    environment_id: UUID

    class Config:
        orm_mode = True
