from typing import List, Generator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.broker.broker import consume
from db.config import DOCKER_KAFKA_TOPIC
from docker.crud.crud_volumes import (get_all_docker_volumes, get_docker_volume)
from docker.client.client_volumes import (create_volume, remove_volume, prune_volumes)
from docker.schemas.schemas_volumes import VolumeInspect, VolumeInspectList
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.schemas.schemas_response import GenericResponseModel
from modules.utils.docker.utils import get_docker_object_by_id
from modules.utils.utils import is_equal


async def get_all_volumes_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[List[VolumeInspect]]:
    crud_volumes = await get_all_docker_volumes(
        node_id=node_id,
        session=session
    )

    return GenericResponseModel(
        data=crud_volumes.volumes,
        total=crud_volumes.total
    )


async def get_volume_from_db(
        node_id: UUID,
        volume_id: str,
        session: AsyncSession
) -> GenericResponseModel[VolumeInspect]:
    crud_volume = await get_docker_volume(
        node_id=node_id,
        session=session,
        volume_id=volume_id
    )

    return GenericResponseModel(
        data=crud_volume.dict(),
        total=1
    )


async def get_all_volumes_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[List[VolumeInspect]],
    GenericResponseModel[List[VolumeInspect]],
    None
]:
    volumes_data = ''
    async for message in consume(topic=DOCKER_KAFKA_TOPIC):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            volumes = snapshot.docker.volumes

            if not is_equal(old_object=volumes_data, new_object=volumes.data):
                volumes_data = volumes.data

                yield GenericResponseModel(
                    data=volumes.data,
                    total=volumes.total
                )


async def get_volume_from_broker(
        node_id: UUID,
        volume_id: str
) -> Generator[
    GenericResponseModel[VolumeInspect],
    GenericResponseModel[VolumeInspect],
    None
]:
    volume_data = ''
    async for message in consume(topic=DOCKER_KAFKA_TOPIC):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            all_volumes = VolumeInspectList(
                volumes=snapshot.docker.volumes.data,
                total=snapshot.docker.volumes.total
            )

            volume = get_docker_object_by_id(
                object_id=volume_id,
                docker_object=all_volumes.volumes
            )

            if not is_equal(old_object=volume_data, new_object=volume.dict()):
                volume_data = volume.dict()

                yield GenericResponseModel(
                    data=volume,
                    total=1
                )


async def create_new_volume(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await create_volume(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def prune_unused_volumes(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await prune_volumes(
        ssh_session=host_ssh_session,
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def remove_volume_by_id(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await remove_volume(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj
