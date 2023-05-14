from typing import Dict

from asyncssh import SSHTCPSession

from config.agent_config import (DOCKER_NETWORK, DOCKER_NETWORK_CREATE,
                                 DOCKER_NETWORK_PRUNE, DOCKER_NETWORK_CONNECT, DOCKER_NETWORK_DISCONNECT)
from docker.schemas.schemas_networks import NetworkCreate, NetworkConnectContainer, NetworkDisconnectContainer


async def create_network(
        ssh_session: SSHTCPSession,
        config: NetworkCreate,
) -> Dict:
    data = config.dict()

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{DOCKER_NETWORK}/{DOCKER_NETWORK_CREATE}',
        data=data
    )

    return response


async def prune_networks(
        ssh_session: SSHTCPSession
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{DOCKER_NETWORK}/{DOCKER_NETWORK_PRUNE}'
    )

    return response


async def connect_network(
        ssh_session: SSHTCPSession,
        network_id: str,
        config: NetworkConnectContainer,
) -> Dict:
    data = config.dict()

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{DOCKER_NETWORK}/{network_id}/{DOCKER_NETWORK_CONNECT}',
        data=data
    )

    return response


async def disconnect_network(
        ssh_session: SSHTCPSession,
        network_id: str,
        config: NetworkDisconnectContainer,
) -> Dict:
    data = config.dict()

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{DOCKER_NETWORK}/{network_id}/{DOCKER_NETWORK_DISCONNECT}',
        data=data
    )

    return response


async def remove_network(
        ssh_session: SSHTCPSession,
        network_id: str,
        **kwargs
) -> Dict:
    response = await ssh_session.delete(
        router='/delete_resource',
        target_resource=f'{DOCKER_NETWORK}/{network_id}',
        params=kwargs
    )

    return response
