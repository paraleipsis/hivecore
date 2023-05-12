from typing import List, Generator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.broker.broker import consume
from db.storage_config import DOCKER_PLATFORM_NAME
from docker.crud.crud_networks import (get_all_docker_networks, get_docker_network)
from docker.client.client_networks import (create_network, remove_network, connect_network,
                                           disconnect_network, prune_networks)
from docker.schemas.schemas_networks import NetworkInspect, NetworkInspectList
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.schemas.schemas_response import GenericResponseModel
from modules.utils.docker.utils import get_docker_object_by_id
from modules.utils.utils import is_equal


async def get_all_networks_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[List[NetworkInspect]]:
    crud_networks = await get_all_docker_networks(
        node_id=node_id,
        session=session
    )

    return GenericResponseModel(
        data=crud_networks.networks,
        total=crud_networks.total
    )


async def get_network_from_db(
        node_id: UUID,
        network_id: str,
        session: AsyncSession
) -> GenericResponseModel[NetworkInspect]:
    crud_network = await get_docker_network(
        node_id=node_id,
        session=session,
        network_id=network_id
    )

    return GenericResponseModel(
        data=crud_network.dict(),
        total=1
    )


async def get_all_networks_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[List[NetworkInspect]],
    GenericResponseModel[List[NetworkInspect]],
    None
]:
    networks_data = ''
    async for message in consume(topic=DOCKER_PLATFORM_NAME):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            networks = snapshot.docker.networks

            if not is_equal(old_object=networks_data, new_object=networks.data):
                networks_data = networks.data

                yield GenericResponseModel(
                    data=networks.data,
                    total=networks.total
                )


async def get_network_from_broker(
        node_id: UUID,
        network_id: str
) -> Generator[
    GenericResponseModel[NetworkInspect],
    GenericResponseModel[NetworkInspect],
    None
]:
    network_data = ''
    async for message in consume(topic=DOCKER_PLATFORM_NAME):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            all_networks = NetworkInspectList(
                networks=snapshot.docker.networks.data,
                total=snapshot.docker.networks.total
            )

            network = get_docker_object_by_id(
                object_id=network_id,
                docker_object=all_networks.networks
            )

            if not is_equal(old_object=network_data, new_object=network.dict()):
                network_data = network.dict()

                yield GenericResponseModel(
                    data=network,
                    total=1
                )


async def create_new_network(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await create_network(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def prune_unused_networks(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await prune_networks(
        ssh_session=host_ssh_session,
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def connect_container_to_network(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await connect_network(
        ssh_session=host_ssh_session,
        **kwargs
    )
    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def disconnect_container_from_network(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await disconnect_network(
        ssh_session=host_ssh_session,
        **kwargs
    )
    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def remove_network_by_id(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await remove_network(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj
