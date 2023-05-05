from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from docker.crud.crud_snapshots import get_docker_snapshot
from docker.schemas.schemas_images import ImageInspectList, ImageInspect
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.utils.docker.utils import get_docker_object_by_id


async def get_all_docker_images(
        node_id: UUID,
        session: AsyncSession
) -> ImageInspectList:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    all_images = ImageInspectList(
        images=snapshot.docker.images.data,
        total=snapshot.docker.images.total
    )

    return all_images


async def get_docker_image(
        node_id: UUID,
        session: AsyncSession,
        images_id: str
) -> ImageInspect:
    all_images = await get_all_docker_images(
        node_id=node_id,
        session=session
    )

    image = get_docker_object_by_id(
        object_id=images_id,
        docker_object=all_images.images
    )

    return image
