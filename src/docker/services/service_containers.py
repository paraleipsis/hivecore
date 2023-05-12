import json
from typing import List, Generator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.broker.broker import consume
from db.storage_config import DOCKER_PLATFORM_NAME
from docker.client.client_containers import (start_container, stop_container, restart_container,
                                             pause_container, unpause_container, kill_container,
                                             prune_containers, remove_container, logs_container, stats_container,
                                             run_container)
from docker.crud.crud_containers import get_all_docker_containers, get_docker_container
from docker.schemas.schemas_containers import ContainerInspect, ContainerInspectList
from docker.schemas.schemas_containers_stats import ContainerStats
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.schemas.schemas_response import GenericResponseModel
from modules.utils.docker.utils import get_docker_object_by_id
from modules.utils.utils import is_equal


async def get_all_containers_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[List[ContainerInspect]]:
    crud_containers = await get_all_docker_containers(
        node_id=node_id,
        session=session
    )

    return GenericResponseModel(
        data=crud_containers.containers,
        total=crud_containers.total
    )


async def get_container_from_db(
        node_id: UUID,
        container_id: str,
        session: AsyncSession
) -> GenericResponseModel[ContainerInspect]:
    crud_container = await get_docker_container(
        node_id=node_id,
        session=session,
        container_id=container_id
    )

    return GenericResponseModel(
        data=crud_container.dict(),
        total=1
    )


async def get_all_containers_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[List[ContainerInspect]],
    GenericResponseModel[List[ContainerInspect]],
    None
]:
    containers_data = ''
    async for message in consume(topic=DOCKER_PLATFORM_NAME):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            containers = snapshot.docker.containers

            if not is_equal(old_object=containers_data, new_object=containers.data):
                containers_data = containers.data

                yield GenericResponseModel(
                    data=containers.data,
                    total=containers.total
                )


async def get_container_from_broker(
        node_id: UUID,
        container_id: str
) -> Generator[
    GenericResponseModel[ContainerInspect],
    GenericResponseModel[ContainerInspect],
    None
]:
    container_data = ''
    async for message in consume(topic=DOCKER_PLATFORM_NAME):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            all_containers = ContainerInspectList(
                containers=snapshot.docker.containers.data,
                total=snapshot.docker.containers.total
            )

            container = get_docker_object_by_id(
                object_id=container_id,
                docker_object=all_containers.containers
            )

            if not is_equal(old_object=container_data, new_object=container.dict()):
                container_data = container.dict()

                yield GenericResponseModel(
                    data=container,
                    total=1
                )


async def start_container_by_id(
        container_id: str,
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await start_container(
        ssh_session=host_ssh_session,
        container_id=container_id
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def stop_container_by_id(
        container_id: str,
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await stop_container(
        ssh_session=host_ssh_session,
        container_id=container_id
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def restart_container_by_id(
        container_id: str,
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await restart_container(
        ssh_session=host_ssh_session,
        container_id=container_id
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def pause_container_by_id(
        container_id: str,
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await pause_container(
        ssh_session=host_ssh_session,
        container_id=container_id
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def unpause_container_by_id(
        container_id: str,
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await unpause_container(
        ssh_session=host_ssh_session,
        container_id=container_id
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def kill_container_by_id(
        container_id: str,
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await kill_container(
        ssh_session=host_ssh_session,
        container_id=container_id
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def remove_container_by_id(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await remove_container(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def run_new_container(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await run_container(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def prune_stopped_containers(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await prune_containers(
        ssh_session=host_ssh_session,
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def logs_container_by_id(
        host_uuid: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient,
) -> Generator[str, str, None]:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']

    async for msg in logs_container(
            container_id=container_id,
            ssh_session=host_ssh_session
    ):
        yield msg['response']


async def stats_container_by_id(
        host_uuid: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient,
) -> Generator[ContainerStats, ContainerStats, None]:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']

    async for msg in stats_container(
            container_id=container_id,
            ssh_session=host_ssh_session
    ):
        stats = ContainerStats(**json.loads(msg['response']))
        yield stats


# async def terminal_container_by_id(
#         host_uuid: UUID,
#         container_id: str,
#         rssh_client: ReverseSSHClient,
#         websocket: WebSocket,
# ) -> GenericResponseModel:
#     host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
#
#     task1 = asyncio.create_task(read_terminal(ssh_session=host_ssh_session, ws=websocket))
#     task2 = asyncio.create_task(write_terminal(ssh_session=host_ssh_session, ws=websocket))
#     await asyncio.gather(task1, task2)
#
#     return response_obj
