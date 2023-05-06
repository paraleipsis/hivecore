from typing import Mapping, List, Optional

from pydantic import BaseModel


class ContainerPidsStats(BaseModel):
    current: Optional[int]


class ContainerNetworksStats(BaseModel):
    rx_bytes: Optional[int]
    rx_dropped: Optional[int]
    rx_errors: Optional[int]
    rx_packets: Optional[int]
    tx_bytes: Optional[int]
    tx_dropped: Optional[int]
    tx_errors: Optional[int]
    tx_packets: Optional[int]


class ContainerMemoryStatsStats(BaseModel):
    cache: Optional[int]


class ContainerMemoryStats(BaseModel):
    stats: Optional[ContainerMemoryStatsStats]
    max_usage: Optional[int]
    usage: Optional[int]
    failcnt: Optional[int]
    limit: Optional[int]


class ContainerCPUUsage(BaseModel):
    percpu_usage: Optional[List[int]]
    usage_in_usermode: int
    total_usage: int
    usage_in_kernelmode: int


class ContainerThrottlingData(BaseModel):
    periods: int
    throttled_periods: int
    throttled_time: int


class ContainerCPUStats(BaseModel):
    cpu_usage: Optional[ContainerCPUUsage]
    system_cpu_usage: Optional[int]
    online_cpus: Optional[int]
    throttling_data: Optional[ContainerThrottlingData]


class ContainerStats(BaseModel):
    read: Optional[str]
    pids_stats: Optional[ContainerPidsStats]
    networks: Mapping[str, ContainerNetworksStats]
    memory_stats: Optional[ContainerMemoryStats]
    cpu_stats: Optional[ContainerCPUStats]
    precpu_stats: Optional[ContainerCPUStats]
