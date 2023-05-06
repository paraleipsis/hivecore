from pydantic import BaseModel
from typing import Optional, List, Mapping


class AuthCredentials(BaseModel):
    username: str
    password: Optional[str]
    email: Optional[str]
    serveraddress: Optional[str]


class AuthToken(BaseModel):
    Status: Optional[str]
    IdentityToken: Optional[str]


class AuthError(BaseModel):
    message: Optional[str]


class SystemInfo(BaseModel):
    ID: Optional[str]
    Containers: Optional[int]
    ContainersRunning: Optional[int]
    ContainersPaused: Optional[int]
    ContainersStopped: Optional[int]
    Images: Optional[int]
    Driver: Optional[str]
    DriverStatus: Optional[List[List[str]]]
    DockerRootDir: Optional[str]
    Plugins: Optional[Mapping]
    MemoryLimit: Optional[bool]
    SwapLimit: Optional[bool]
    KernelMemoryTCP: Optional[bool]
    CpuCfsPeriod: Optional[bool]
    CpuCfsQuota: Optional[bool]
    CPUShares: Optional[bool]
    CPUSet: Optional[bool]
    PidsLimit: Optional[bool]
    OomKillDisable: Optional[bool]
    IPv4Forwarding: Optional[bool]
    BridgeNfIptables: Optional[bool]
    BridgeNfIp6tables: Optional[bool]
    Debug: Optional[bool]
    NFd: Optional[int]
    NGoroutines: Optional[int]
    SystemTime: Optional[str]
    LoggingDriver: Optional[str]
    CgroupDriver: Optional[str]
    CgroupVersion: Optional[str]
    NEventsListener: Optional[int]
    KernelVersion: Optional[str]
    OperatingSystem: Optional[str]
    OSVersion: Optional[str]
    OSType: Optional[str]
    Architecture: Optional[str]
    NCPU: Optional[int]
    MemTotal: Optional[int]
    IndexServerAddress: Optional[str]
    RegistryConfig: Optional[Mapping]
    GenericResources: Optional[List[Mapping]]
    HttpProxy: Optional[str]
    HttpsProxy: Optional[str]
    NoProxy: Optional[str]
    Name: Optional[str]
    Labels: Optional[List[str]]
    ExperimentalBuild: Optional[bool]
    ServerVersion: Optional[str]
    ClusterStore: Optional[str]
    ClusterAdvertise: Optional[str]
    Runtimes: Optional[Mapping]
    DefaultRuntime: Optional[str]
    Swarm: Optional[Mapping]
    LiveRestoreEnabled: Optional[bool]
    Isolation: Optional[str]
    InitBinary: Optional[str]
    ContainerdCommit: Optional[Mapping]
    RuncCommit: Optional[Mapping]
    InitCommit: Optional[Mapping]
    SecurityOptions: Optional[List[str]]
    ProductLicense: Optional[str]
    DefaultAddressPools: Optional[List[Mapping]]
    Warnings: Optional[List[str]]


class SystemVersion(BaseModel):
    Platform: Optional[Mapping]
    Components: Optional[List[Mapping]]
    Version: Optional[str]
    ApiVersion: Optional[str]
    MinAPIVersion: Optional[str]
    GitCommit: Optional[str]
    GoVersion: Optional[str]
    Os: Optional[str]
    Arch: Optional[str]
    KernelVersion: Optional[str]
    Experimental: Optional[bool]
    BuildTime: Optional[str]


class SystemDF(BaseModel):
    LayersSize: Optional[int]
    Images: Optional[List[Mapping]]
    Containers: Optional[List[Mapping]]
    Volumes: Optional[List[Mapping]]
    BuildCache: Optional[List[Mapping]]
