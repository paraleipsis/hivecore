from typing import List
from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

from node_manager.schemas.schemas_clusters import ClusterRead
from node_manager.schemas.schemas_nodes import NodeRead


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


class PlatformNodesRead(PlatformRead):
    nodes: List[NodeRead]

    class Config:
        orm_mode = True


class PlatformClustersRead(PlatformRead):
    clusters: List[ClusterRead]

    class Config:
        orm_mode = True
