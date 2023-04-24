from typing import Mapping, List, Optional

from pydantic import BaseModel


class ContainerPidsStats(BaseModel):
    current: int


class ContainerNetworksStats(BaseModel):
    rx_bytes: int
    rx_dropped: int
    rx_errors: int
    rx_packets: int
    tx_bytes: int
    tx_dropped: int
    tx_errors: int
    tx_packets: int


class ContainerMemoryStatsStats(BaseModel):
    cache: int


class ContainerMemoryStats(BaseModel):
    stats: Optional[ContainerMemoryStatsStats]
    max_usage: Optional[int]
    usage: int
    failcnt: Optional[int]
    limit: int


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
    cpu_usage: ContainerCPUUsage
    system_cpu_usage: int
    online_cpus: int
    throttling_data: ContainerThrottlingData


class ContainerStats(BaseModel):
    read: str
    pids_stats: ContainerPidsStats
    networks: Mapping[str, ContainerNetworksStats]
    memory_stats: ContainerMemoryStats
    cpu_stats: ContainerCPUStats
    precpu_stats: ContainerCPUStats
