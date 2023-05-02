from typing import Dict

from asyncssh import SSHTCPSession
from config.agent_config import DOCKER_START_CONTAINER, AGENT_URL


async def start_container(ssh_session: SSHTCPSession, container_id: str) -> Dict:
    start_endpoint = DOCKER_START_CONTAINER.format(container_id)
    response = await ssh_session.post(
        router='/post_resource',
        data={
            'target_resource': f'{AGENT_URL}/{start_endpoint}'
        }
    )

    return response
