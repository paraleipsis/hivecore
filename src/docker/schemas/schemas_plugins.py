from pydantic import BaseModel, Field
from typing import Optional, List, Mapping


class PluginInstall(BaseModel):
    Name: Optional[str]
    Description: Optional[str]
    Value: Optional[List]


class PluginInspect(BaseModel):
    Id: Optional[str]
    Name: Optional[str]
    Enabled: Optional[bool]
    Settings: Optional[Mapping]
    PluginReference: Optional[str]
    PluginConfig: Optional[Mapping] = Field(default=None, alias="Config")


class PluginInspectList(BaseModel):
    plugins: List[PluginInspect]
    total: int
