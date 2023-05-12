import ipaddress
from typing import Optional, Mapping
from uuid import UUID

from pydantic import BaseModel, validator
from datetime import datetime


class NodeBase(BaseModel):
    name: str
    description: Optional[str]
    server_ipv4: str

    @validator("server_ipv4")
    def ipv4_validation(cls, v):
        ipaddress.IPv4Address(v)
        return v


class NodeCreate(NodeBase):
    pass


class NodeRead(NodeBase):
    id: UUID
    created_at: datetime
    active: bool = False

    class Config:
        orm_mode = True


class NodePlatformCreate(BaseModel):
    node_id: UUID
    platform_name: str


class NodePlatformRead(BaseModel):
    id: UUID
    node_id: UUID
    platform_name: str

    class Config:
        orm_mode = True


class NodeSnapshotBase(BaseModel):
    snapshot: Mapping


class NodeSnapshotRead(NodeSnapshotBase):
    id: UUID
    created_at: datetime
    node_id: UUID
    platform_name: str

    class Config:
        orm_mode = True
