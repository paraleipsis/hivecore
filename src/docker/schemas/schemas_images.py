from typing import List, Optional, Mapping, Any

from pydantic import BaseModel, Field


class ImageCreate(BaseModel):
    remote: Optional[str]
    fileobj: Optional[str]
    tag: Optional[str]
    nocache: Optional[bool] = False
    pull: Optional[bool] = False
    rm: Optional[bool] = True
    forcerm: Optional[bool] = False
    labels: Optional[Mapping]

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """Override the default dict method to exclude None values in the response."""

        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)


class ImageInspect(BaseModel):
    Id: Optional[str]
    RepoTags: Optional[List[str]]
    RepoDigests: Optional[List[str]]
    Parent: Optional[str]
    Comment: Optional[str]
    Created: Optional[str]
    Container: Optional[str]
    ContainerConfig: Optional[Mapping]
    DockerVersion: Optional[str]
    Author: Optional[str]
    ImageConfig: Optional[Mapping] = Field(default=None, alias="Config")
    Architecture: Optional[str]
    Variant: Optional[str]
    Os: Optional[str]
    OsVersion: Optional[str]
    Size: Optional[int]
    VirtualSize: Optional[int]
    GraphDriver: Optional[Mapping]
    RootFS: Optional[Mapping]
    Metadata: Optional[Mapping]


class ImageInspectList(BaseModel):
    images: List[ImageInspect]
    total: int
