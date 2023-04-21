from pydantic import BaseModel, Field
from datetime import datetime
from typing import Generic, TypeVar, Optional, List
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class GenericResponseModel(GenericModel, Generic[DataT]):
    success: bool = Field(True)
    error_msg: Optional[str] = Field(None, alias='errorMsg')
    data: Optional[DataT] = Field(None)
    total: Optional[int] = Field(None)

    class Config:
        allow_population_by_field_name = True


class PlatformBase(BaseModel):
    name: str
    description: str
    type: str


class EnvironmentBase(BaseModel):
    name: str
    description: str


class NodeBase(BaseModel):
    name: str
    description: str
    node_ip: str


class PlatformCreate(PlatformBase):
    pass


class EnvironmentCreate(EnvironmentBase):
    pass


class NodeCreate(NodeBase):
    pass


class NodeRead(NodeBase):
    id: int
    created_at: datetime
    environment_id: int

    class Config:
        orm_mode = True


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
