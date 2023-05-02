import ipaddress

from typing import Optional, Mapping, Literal, List
from pydantic import BaseModel, validator, Field


class ContainerVolumeBind(BaseModel):
    host_path: str
    container_path: str
    mode: Optional[Literal['ro', 'rw']]
    shared_mount: Optional[bool]


class ContainerPortsBind(BaseModel):
    host_port: str
    container_port: str
    tcp: Optional[bool] = True
    udp: Optional[bool] = False


class DeviceRequests(BaseModel):
    Driver: str
    Count: Optional[int]
    DeviceIDs: Optional[List]
    Capabilities: Optional[List[List[str]]]
    Options: Optional[Mapping]


class HostPortMapping(BaseModel):
    HostPort: str


class RestartPolicy(BaseModel):
    Name: str
    MaximumRetryCount: int


class LogConfig(BaseModel):
    Type: Literal[
        'awslogs', 'fluentd', 'gcplogs', 'gelf', 'journald',
        'json-file', 'local', 'logentries', 'splunk', 'syslog'
    ]
    ConfigLog: Optional[Mapping] = Field(None, alias='Config')


class HostConfig(BaseModel):
    Binds: Optional[List[str]]
    Links: Optional[List[str]]
    Memory: Optional[int]
    MemorySwap: Optional[int]
    MemoryReservation: Optional[int]
    NanoCpus: Optional[int]
    CpuPercent: Optional[int]
    CpuShares: Optional[int]
    CpuPeriod: Optional[int]
    CpuRealtimePeriod: Optional[int]
    CpuRealtimeRuntime: Optional[int]
    CpuQuota: Optional[int]
    CpusetCpus: Optional[str]
    CpusetMems: Optional[str]
    MaximumIOps: Optional[int]
    MaximumIOBps: Optional[int]
    BlkioWeight: Optional[int]
    BlkioWeightDevice: Optional[List[Mapping]]
    BlkioDeviceReadBps: Optional[List[Mapping]]
    BlkioDeviceReadIOps: Optional[List[Mapping]]
    BlkioDeviceWriteBps: Optional[List[Mapping]]
    BlkioDeviceWriteIOps: Optional[List[Mapping]]
    DeviceRequests: Optional[List[DeviceRequests]]
    MemorySwappiness: Optional[int]
    OomKillDisable: Optional[bool]
    OomScoreAdj: Optional[int]
    PidMode: Optional[str]
    PidsLimit: Optional[int]
    PortBindings: Optional[Mapping[str, List[HostPortMapping]]]
    PublishAllPorts: Optional[bool]
    Privileged: Optional[bool]
    ReadonlyRootfs: Optional[bool]
    Dns: Optional[List[str]]
    DnsOptions: Optional[List[str]]
    DnsSearch: Optional[List[str]]
    VolumesFrom: Optional[List[str]]
    CapAdd: Optional[List[str]]
    CapDrop: Optional[List[str]]
    GroupAdd: Optional[List[str]]
    RestartPolicy: Optional[RestartPolicy]
    AutoRemove: Optional[bool]
    # TODO: add support for dynamic network modes collecting from appropriate host
    NetworkMode: Optional[Literal['bridge', 'host', 'overlay', 'ipvlan', 'macvlan', 'none']]
    Devices: Optional[List]
    Ulimits: Optional[List[Mapping]]
    # TODO: add support for dynamic log drivers collecting from appropriate host
    LogConfig: LogConfig
    SecurityOpt: Optional[List]
    StorageOpt: Optional[Mapping]
    CgroupParent: Optional[str]
    # TODO: add support for dynamic volume drivers collecting from appropriate host
    VolumeDriver: Optional[Literal['local']]
    ShmSize: Optional[int]


class IPAMConfig(BaseModel):
    IPv4Address: str
    IPv6Address: Optional[str]
    LinkLocalIPs: Optional[List[str]]

    @validator('IPv4Address')
    def ipv4_validation(cls, v):
        ipaddress.IPv4Address(v)
        return v

    @validator('IPv6Address')
    def ipv6_validation(cls, v):
        ipaddress.IPv6Address(v)
        return v


class EndpointConfig(BaseModel):
    IPAMConfig: IPAMConfig
    Links: Optional[List[str]]
    Aliases: Optional[List[str]]


class NetworkingConfig(BaseModel):
    EndpointsConfig: Mapping[str, EndpointConfig]


class ContainerBase(BaseModel):
    Image: str
    Labels: Optional[Mapping]
    HostConfig: Optional[Mapping]


class ContainerConfig(BaseModel):
    Hostname: Optional[str]
    Domainname: Optional[str]
    User: Optional[str]
    AttachStdin: Optional[bool]
    AttachStdout: Optional[bool]
    AttachStderr: Optional[bool]
    Tty: Optional[bool]
    OpenStdin: Optional[bool]
    StdinOnce: Optional[bool]
    Cmd: Optional[List[str]]
    # TODO: fix for empty dict
    Volumes: Optional[Mapping[str, Mapping[str, str]]]
    WorkingDir: Optional[str]
    NetworkDisabled: Optional[bool]
    MacAddress: Optional[str]
    StopSignal: Optional[str]
    StopTimeout: Optional[int]


class ContainerPorts(BaseModel):
    PrivatePort: int
    PublicPort: int
    Type: str


class ContainerNetworks(BaseModel):
    NetworkID: str
    EndpointID: str
    Gateway: str
    IPAddress: str
    IPPrefixLen: int
    IPv6Gateway: str
    GlobalIPv6Address: str
    GlobalIPv6PrefixLen: int
    MacAddress: str


class ContainerNetworkSettings(BaseModel):
    Bridge: Optional[str]
    SandboxID: Optional[str]
    HairpinMode: Optional[bool]
    LinkLocalIPv6Address: Optional[str]
    LinkLocalIPv6PrefixLen:  Optional[int]
    SandboxKey: Optional[str]
    EndpointID: Optional[str]
    Gateway: Optional[str]
    GlobalIPv6Address: Optional[str]
    GlobalIPv6PrefixLen: Optional[int]
    IPAddress: Optional[str]
    IPPrefixLen: Optional[int]
    IPv6Gateway: Optional[str]
    MacAddress: Optional[str]
    Networks: Mapping[str, ContainerNetworks]


class ContainerMounts(BaseModel):
    Type: Literal['bind', 'volume', 'tmpfs', 'npipe']
    Name: str
    Source: str
    Destination: str
    Driver: str
    Mode: str
    RW: bool
    Propagation: Literal['rprivate', 'private', 'rshared', 'shared', 'rslave', 'slave']


class ContainerHealthLog(BaseModel):
    Start: str
    End: str
    ExitCode: int
    Output: str


class ContainerHealth(BaseModel):
    Status: Literal['healthy', 'unhealthy', 'starting']
    FailingStreak: int
    Log: Optional[List[ContainerHealthLog]]


class ContainerState(BaseModel):
    Error: str
    ExitCode: int
    FinishedAt: str
    Health: Optional[ContainerHealth]
    OOMKilled: bool
    Dead: bool
    Paused: bool
    Pid: int
    Restarting: bool
    Running: bool
    StartedAt: str
    Status: str


class ContainerCreate(ContainerBase, ContainerConfig):
    # custom Env mapping binding: host-agent parses and converts it into list of strings - 'env=value'
    Env: Optional[Mapping[str, str]]
    Entrypoint: Optional[str]
    # custom Volumes binding: host-agent parses and converts it into Docker binding
    VolumesBind: Optional[ContainerVolumeBind]
    # TODO: fix for empty dict
    ExposedPorts: Optional[Mapping[str, Mapping[str, str]]]
    # custom Ports binding: host-agent parses and converts it into Docker binding
    PortsBind: Optional[ContainerPortsBind]
    NetworkingConfig: Optional[NetworkingConfig]


class Container(ContainerBase):
    Id: str
    Names: List[str]
    ImageID: str
    Command: str
    Created: int
    State: str
    Status: str
    Ports: List[Mapping]
    SizeRw: int
    SizeRootFs: int
    NetworkSettings: Mapping
    Mounts: List[Mapping]


class ContainerInspect(ContainerBase):
    AppArmorProfile: Optional[str]
    Args: Optional[List[str]]
    ContainerConfigs: Optional[Mapping] = Field(default=None, alias='Config')
    Created: Optional[str]
    Driver: Optional[str]
    ExecIDs: Optional[List[str]]
    HostnamePath: Optional[str]
    HostsPath: Optional[str]
    LogPath: Optional[str]
    Id: Optional[str]
    MountLabel: Optional[str]
    Name: str
    NetworkSettings: Optional[Mapping]
    Path: Optional[str]
    ProcessLabel: Optional[str]
    ResolvConfPath: Optional[str]
    RestartCount: Optional[int]
    State: Optional[Mapping]
    Mounts: Optional[List[Mapping]]
