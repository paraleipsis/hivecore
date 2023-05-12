from typing import List, Generator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.broker.broker import consume
from db.storage_config import DOCKER_PLATFORM_NAME
from docker.crud.crud_plugins import (get_all_docker_plugins, get_docker_plugin)
from docker.client.client_plugins import (install_plugin, remove_plugin, enable_plugin, disable_plugin)
from docker.schemas.schemas_plugins import PluginInspect, PluginInspectList
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.schemas.schemas_response import GenericResponseModel
from modules.utils.docker.utils import get_docker_object_by_id
from modules.utils.utils import is_equal


async def get_all_plugins_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[List[PluginInspect]]:
    crud_plugins = await get_all_docker_plugins(
        node_id=node_id,
        session=session
    )

    return GenericResponseModel(
        data=crud_plugins.plugins,
        total=crud_plugins.total
    )


async def get_plugin_from_db(
        node_id: UUID,
        plugin_id: str,
        session: AsyncSession
) -> GenericResponseModel[PluginInspect]:
    crud_plugin = await get_docker_plugin(
        node_id=node_id,
        session=session,
        plugin_id=plugin_id
    )

    return GenericResponseModel(
        data=crud_plugin.dict(),
        total=1
    )


async def get_all_plugins_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[List[PluginInspect]],
    GenericResponseModel[List[PluginInspect]],
    None
]:
    plugins_data = ''
    async for message in consume(topic=DOCKER_PLATFORM_NAME):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            plugins = snapshot.docker.plugins

            if not is_equal(old_object=plugins_data, new_object=plugins.data):
                plugins_data = plugins.data

                yield GenericResponseModel(
                    data=plugins.data,
                    total=plugins.total
                )


async def get_plugin_from_broker(
        node_id: UUID,
        plugin_id: str
) -> Generator[
    GenericResponseModel[PluginInspect],
    GenericResponseModel[PluginInspect],
    None
]:
    plugin_data = ''
    async for message in consume(topic=DOCKER_PLATFORM_NAME):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            all_plugins = PluginInspectList(
                plugins=snapshot.docker.plugins.data,
                total=snapshot.docker.plugins.total
            )

            plugin = get_docker_object_by_id(
                object_id=plugin_id,
                docker_object=all_plugins.plugins
            )

            if not is_equal(old_object=plugin_data, new_object=plugin.dict()):
                plugin_data = plugin.dict()

                yield GenericResponseModel(
                    data=plugin,
                    total=1
                )


async def install_new_plugin(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await install_plugin(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def enable_plugin_by_id(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await enable_plugin(
        ssh_session=host_ssh_session,
        **kwargs
    )
    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def disable_plugin_by_id(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await disable_plugin(
        ssh_session=host_ssh_session,
        **kwargs
    )
    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def remove_plugin_by_id(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await remove_plugin(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj
