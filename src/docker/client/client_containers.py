from typing import Dict, Generator

from asyncssh import SSHTCPSession

from config.agent_config import (AGENT_URL, DOCKER_CONTAINER_START, DOCKER_CONTAINER_STOP,
                                 DOCKER_CONTAINER_RESTART, DOCKER_CONTAINER_PAUSE, DOCKER_CONTAINER_UNPAUSE,
                                 DOCKER_CONTAINER_KILL, DOCKER_CONTAINER_PRUNE, DOCKER_CONTAINER, DOCKER_CONTAINER_LOGS,
                                 DOCKER_CONTAINER_STATS, DOCKER_CONTAINER_RUN)
from docker.schemas.schemas_containers import ContainerCreate


async def run_container(
        ssh_session: SSHTCPSession,
        config: ContainerCreate,
        **kwargs
) -> Dict:
    data = config.dict()

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{DOCKER_CONTAINER_RUN}',
        params=kwargs,
        data=data
    )

    return response


async def start_container(
        ssh_session: SSHTCPSession,
        container_id: str
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_START}'
    )

    return response


async def stop_container(
        ssh_session: SSHTCPSession,
        container_id: str
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_STOP}'
    )

    return response


async def restart_container(
        ssh_session: SSHTCPSession,
        container_id: str
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_RESTART}'
    )

    return response


async def pause_container(
        ssh_session: SSHTCPSession,
        container_id: str
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_PAUSE}'
    )

    return response


async def unpause_container(
        ssh_session: SSHTCPSession,
        container_id: str
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_UNPAUSE}'
    )

    return response


async def kill_container(
        ssh_session: SSHTCPSession,
        container_id: str
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_KILL}'
    )

    return response


async def remove_container(
        ssh_session: SSHTCPSession,
        container_id: str,
        **kwargs
) -> Dict:
    response = await ssh_session.delete(
        router='/delete_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}',
        params=kwargs
    )

    return response


async def prune_containers(
        ssh_session: SSHTCPSession
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{DOCKER_CONTAINER_PRUNE}'
    )

    return response


async def logs_container(
        ssh_session: SSHTCPSession,
        container_id: str,
) -> Generator[Dict, Dict, None]:
    async for msg in ssh_session.stream(
            router='/ws_resource',
            target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_LOGS}',
    ):
        yield msg


async def stats_container(
        ssh_session: SSHTCPSession,
        container_id: str,
) -> Generator[Dict, Dict, None]:
    async for msg in ssh_session.stream(
            router='/ws_resource',
            target_resource=f'{AGENT_URL}/{DOCKER_CONTAINER}/{container_id}/{DOCKER_CONTAINER_STATS}',
    ):
        yield msg
