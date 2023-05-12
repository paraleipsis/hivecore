from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

from node_manager.schemas.schemas_nodes import NodeRead


class ClusterBase(BaseModel):
    id: UUID
    name: Optional[str]
    description: Optional[str]


class ClusterCreate(ClusterBase):
    pass


class ClusterRead(ClusterBase):
    id: UUID
    created_at: datetime
    platform_id: UUID

    class Config:
        orm_mode = True


class ClusterNodesRead(ClusterRead):
    nodes: List[NodeRead]

    class Config:
        orm_mode = True
