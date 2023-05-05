from typing import List, Generator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.broker.broker import consume
from db.config import DOCKER_KAFKA_TOPIC
from docker.crud.crud_images import (get_all_docker_images, get_docker_image)
from docker.client.client_images import (build_image, prune_images, pull_image, tag_image, remove_image)
from docker.schemas.schemas_images import ImageInspect, ImageInspectList
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.schemas.schemas_response import GenericResponseModel
from modules.utils.docker.utils import get_docker_object_by_id
from modules.utils.utils import is_equal


async def get_all_images_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[List[ImageInspect]]:
    crud_images = await get_all_docker_images(
        node_id=node_id,
        session=session
    )

    return GenericResponseModel(
        data=crud_images.images,
        total=crud_images.total
    )


async def get_image_from_db(
        node_id: UUID,
        images_id: str,
        session: AsyncSession
) -> GenericResponseModel[ImageInspect]:
    crud_image = await get_docker_image(
        node_id=node_id,
        session=session,
        images_id=images_id
    )

    return GenericResponseModel(
        data=crud_image.dict(),
        total=1
    )


async def get_all_images_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[List[ImageInspect]],
    GenericResponseModel[List[ImageInspect]],
    None
]:
    images_data = ''
    async for message in consume(topic=DOCKER_KAFKA_TOPIC):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            images = snapshot.docker.images

            if not is_equal(old_object=images_data, new_object=images.data):
                images_data = images.data

                yield GenericResponseModel(
                    data=images.data,
                    total=images.total
                )


async def get_image_from_broker(
        node_id: UUID,
        image_id: str
) -> Generator[
    GenericResponseModel[ImageInspect],
    GenericResponseModel[ImageInspect],
    None
]:
    image_data = ''
    async for message in consume(topic=DOCKER_KAFKA_TOPIC):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            all_images = ImageInspectList(
                images=snapshot.docker.images.data,
                total=snapshot.docker.images.total
            )

            image = get_docker_object_by_id(
                object_id=image_id,
                docker_object=all_images.images
            )

            if not is_equal(old_object=image_data, new_object=image.dict()):
                image_data = image.dict()

                yield GenericResponseModel(
                    data=image,
                    total=1
                )


async def build_new_image(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await build_image(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def prune_unused_images(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await prune_images(
        ssh_session=host_ssh_session,
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def pull_new_image(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await pull_image(
        ssh_session=host_ssh_session,
        **kwargs
    )
    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def tag_image_repo(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await tag_image(
        ssh_session=host_ssh_session,
        **kwargs
    )
    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def remove_image_by_id(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await remove_image(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj
