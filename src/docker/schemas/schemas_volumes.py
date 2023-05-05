from pydantic import BaseModel
from typing import Optional, Mapping, List


class VolumeBase(BaseModel):
    Id: str
    Driver: Optional[str]
    Labels: Optional[Mapping]


class VolumeCreate(VolumeBase):
    DriverOpts: Optional[Mapping]
    ClusterVolumeSpec: Optional[Mapping]


class VolumeInspect(VolumeBase):
    Mountpoint: Optional[str]
    CreatedAt: Optional[str]
    Status: Optional[Mapping]
    Scope: Optional[str]
    ClusterVolume: Optional[Mapping]
    Options: Optional[Mapping]
    UsageData: Optional[Mapping]


class VolumeInspectList(BaseModel):
    volumes: List[VolumeInspect]
    total: int
