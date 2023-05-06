from typing import Dict, Generator

from asyncssh import SSHTCPSession

from config.agent_config import (AGENT_URL, DOCKER_SYSTEM, DOCKER_SYSTEM_EVENTS, DOCKER_SYSTEM_PRUNE,
                                 DOCKER_SYSTEM_AUTH)
from docker.schemas.schemas_system import AuthCredentials


async def docker_login(
        ssh_session: SSHTCPSession,
        config: AuthCredentials,
) -> Dict:
    data = config.dict()

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_SYSTEM}/{DOCKER_SYSTEM_AUTH}',
        data=data
    )

    return response


async def prune_system(
        ssh_session: SSHTCPSession,
        volumes: bool = False
) -> Dict:
    params = {'volumes': volumes}

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_SYSTEM}/{DOCKER_SYSTEM_PRUNE}',
        params=params
    )

    return response


async def docker_events(
        ssh_session: SSHTCPSession,
) -> Generator[Dict, Dict, None]:
    async for msg in ssh_session.stream(
            router='/ws_resource',
            target_resource=f'{AGENT_URL}/{DOCKER_SYSTEM}/{DOCKER_SYSTEM_EVENTS}',
    ):
        yield msg
