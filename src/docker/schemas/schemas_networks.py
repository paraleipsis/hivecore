from typing import Optional, Mapping, List

from pydantic import BaseModel, Field

from docker.schemas import schemas_containers


class IPAMConfig(BaseModel):
    Subnet: Optional[str]
    IPRange: Optional[str]
    Gateway: Optional[str]


class IPAM(BaseModel):
    Driver: Optional[str]
    ConfigIPAM: Optional[List[IPAMConfig]] = Field(default=None, alias="Config")
    Options: Optional[Mapping]


class EndpointConfig(BaseModel):
    IPAMConfig: Optional[schemas_containers.IPAMConfig]
    Links: Optional[List[str]]
    DriverOpts: Optional[Mapping]


class NetworkBase(BaseModel):
    Name: str
    Driver: Optional[str]
    Internal: Optional[bool]
    Attachable: Optional[bool]
    Ingress: Optional[bool]
    IPAM: Optional[IPAM]
    EnableIPv6: Optional[bool]
    Options: Optional[Mapping]
    Labels: Optional[Mapping]


class NetworkInspect(NetworkBase):
    Id: str
    Containers: Mapping
    Created: str
    Scope: str


class NetworkCreate(NetworkBase):
    CheckDuplicate: Optional[bool]


class NetworkConnectContainer(BaseModel):
    Container: str
    EndpointConfig: Optional[EndpointConfig]


class NetworkDisconnectContainer(BaseModel):
    Container: str
    Force: Optional[bool]


class NetworkInspectList(BaseModel):
    networks: List[NetworkInspect]
    total: int
