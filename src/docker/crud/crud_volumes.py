from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from docker.crud.crud_snapshots import get_docker_snapshot
from docker.schemas.schemas_volumes import VolumeInspectList, VolumeInspect
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.utils.docker.utils import get_docker_object_by_id


async def get_all_docker_volumes(
        node_id: UUID,
        session: AsyncSession
) -> VolumeInspectList:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    all_volumes = VolumeInspectList(
        volumes=snapshot.docker.volumes.data,
        total=snapshot.docker.volumes.total
    )

    return all_volumes


async def get_docker_volume(
        node_id: UUID,
        session: AsyncSession,
        volume_id: str
) -> VolumeInspect:
    all_volumes = await get_all_docker_volumes(
        node_id=node_id,
        session=session
    )

    volume = get_docker_object_by_id(
        object_id=volume_id,
        docker_object=all_volumes.volumes
    )

    return volume
