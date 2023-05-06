from typing import Dict, List

from asyncssh import SSHTCPSession

from config.agent_config import (AGENT_URL, DOCKER_PLUGIN, DOCKER_PLUGIN_INSTALL, DOCKER_PLUGIN_ENABLE,
                                 DOCKER_PLUGIN_DISABLE)
from docker.schemas.schemas_plugins import PluginInstall


async def install_plugin(
        ssh_session: SSHTCPSession,
        config: List[PluginInstall],
) -> Dict:
    data = [c.dict() for c in config]

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_PLUGIN}/{DOCKER_PLUGIN_INSTALL}',
        data=data
    )

    return response


async def enable_plugin(
        ssh_session: SSHTCPSession,
        plugin_id: str,
        **kwargs
) -> Dict:

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_PLUGIN}/{plugin_id}/{DOCKER_PLUGIN_ENABLE}',
        params=kwargs
    )

    return response


async def disable_plugin(
        ssh_session: SSHTCPSession,
        plugin_id: str,
) -> Dict:

    response = await ssh_session.post(
        router='/post_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_PLUGIN}/{plugin_id}/{DOCKER_PLUGIN_DISABLE}',
    )

    return response


async def remove_plugin(
        ssh_session: SSHTCPSession,
        plugin_id: str,
        **kwargs
) -> Dict:
    response = await ssh_session.delete(
        router='/delete_resource',
        target_resource=f'{AGENT_URL}/{DOCKER_PLUGIN}/{plugin_id}',
        params=kwargs
    )

    return response
