from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from docker.crud.crud_snapshots import get_docker_snapshot
from docker.schemas.schemas_containers import ContainerInspectList, ContainerInspect
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.utils.docker.utils import get_docker_object_by_id


async def get_all_docker_containers(
        node_id: UUID,
        session: AsyncSession
) -> ContainerInspectList:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    all_containers = ContainerInspectList(
        containers=snapshot.docker.containers.data,
        total=snapshot.docker.containers.total
    )

    return all_containers


async def get_docker_container(
        node_id: UUID,
        session: AsyncSession,
        container_id: str
) -> ContainerInspect:
    all_containers = await get_all_docker_containers(
        node_id=node_id,
        session=session
    )

    container = get_docker_object_by_id(
        object_id=container_id,
        docker_object=all_containers.containers
    )

    return container
