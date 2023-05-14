from typing import Dict

from asyncssh import SSHTCPSession

from config.agent_config import (DOCKER_VOLUME, DOCKER_VOLUME_CREATE, DOCKER_VOLUME_PRUNE)
from docker.schemas.schemas_volumes import VolumeCreate


async def create_volume(
        ssh_session: SSHTCPSession,
        config: VolumeCreate,
) -> Dict:
    data = config.dict()

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{DOCKER_VOLUME}/{DOCKER_VOLUME_CREATE}',
        data=data
    )

    return response


async def prune_volumes(
        ssh_session: SSHTCPSession
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{DOCKER_VOLUME}/{DOCKER_VOLUME_PRUNE}'
    )

    return response


async def remove_volume(
        ssh_session: SSHTCPSession,
        volume_id: str,
        **kwargs
) -> Dict:
    response = await ssh_session.delete(
        router='/delete_resource',
        target_resource=f'{DOCKER_VOLUME}/{volume_id}',
        params=kwargs
    )

    return response
