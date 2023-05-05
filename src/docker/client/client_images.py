from typing import Dict

from asyncssh import SSHTCPSession

from config.agent_config import (AGENT_URL, DOCKER_IMAGE, DOCKER_IMAGE_PULL, DOCKER_IMAGE_TAG,
                                 DOCKER_IMAGE_BUILD, DOCKER_IMAGE_PRUNE)
from docker.schemas.schemas_images import ImageCreate
from modules.utils.utils import clean_map


async def build_image(
        ssh_session: SSHTCPSession,
        config: ImageCreate,
) -> Dict:
    data = config.dict()

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_IMAGE}/{DOCKER_IMAGE_BUILD}',
        data=data
    )

    return response


async def prune_images(
        ssh_session: SSHTCPSession
) -> Dict:
    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_IMAGE}/{DOCKER_IMAGE_PRUNE}'
    )

    return response


async def pull_image(
        ssh_session: SSHTCPSession,
        **kwargs
) -> Dict:
    params = clean_map(kwargs)

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_IMAGE}/{DOCKER_IMAGE_PULL}',
        params=params
    )

    return response


async def tag_image(
        ssh_session: SSHTCPSession,
        image_id: str,
        **kwargs
) -> Dict:
    params = clean_map(kwargs)

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_IMAGE}/{image_id}/{DOCKER_IMAGE_TAG}',
        params=params
    )

    return response


async def remove_image(
        ssh_session: SSHTCPSession,
        image_id: str,
        **kwargs
) -> Dict:
    response = await ssh_session.delete(
        router='/delete_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_IMAGE}/{image_id}',
        params=kwargs
    )

    return response
