from typing import List, Generator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.broker.broker import consume
from db.config import DOCKER_KAFKA_TOPIC
from docker.client.client_containers import start_container
from docker.crud.crud_snapshots import get_docker_snapshot
from docker.schemas.schemas_containers import ContainerInspect
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.schemas.schemas_response import GenericResponseModel


async def get_containers_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[List[ContainerInspect]]:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    containers = snapshot.docker.containers

    return GenericResponseModel(
        data=containers.data,
        total=containers.total
    )


async def get_containers_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[List[ContainerInspect]],
    GenericResponseModel[List[ContainerInspect]],
    None
]:
    async for message in consume(topic=DOCKER_KAFKA_TOPIC):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            containers = snapshot.docker.containers
            yield GenericResponseModel(
                data=containers.data,
                total=containers.total
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
