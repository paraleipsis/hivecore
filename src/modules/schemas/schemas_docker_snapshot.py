from pydantic import BaseModel, Field
from typing import Optional, List, Mapping, Union, Literal


class DockerObject(BaseModel):
    data: Union[List[Mapping], Mapping]
    total: Optional[int]


class DockerObjectsSnapshot(BaseModel):
    images: DockerObject
    containers: DockerObject
    volumes: DockerObject
    networks: DockerObject
    system: DockerObject
    df: DockerObject
    version: DockerObject
    plugins: DockerObject
    swarm_mode: Literal['active', 'inactive']
    swarm_role: Optional[Literal['manager', 'worker']] = Field(None)


class SwarmObjectsSnapshot(BaseModel):
    swarm: DockerObject
    services: DockerObject
    tasks: DockerObject
    configs: DockerObject
    secrets: DockerObject
    nodes: DockerObject


class DockerSnapshot(BaseModel):
    docker: DockerObjectsSnapshot
    swarm: Optional[SwarmObjectsSnapshot] = Field(None)
