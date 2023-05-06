from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from docker.crud.crud_snapshots import get_docker_snapshot
from docker.schemas.schemas_system import SystemInfo, SystemVersion, SystemDF
from modules.schemas.schemas_docker_snapshot import DockerSnapshot


async def get_docker_system_info(
        node_id: UUID,
        session: AsyncSession
) -> SystemInfo:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    info = SystemInfo(**snapshot.docker.system.data)

    return info


async def get_docker_system_df(
        node_id: UUID,
        session: AsyncSession
) -> SystemDF:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    df = SystemDF(**snapshot.docker.df.data)

    return df


async def get_docker_version(
        node_id: UUID,
        session: AsyncSession
) -> SystemVersion:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    version = SystemVersion(**snapshot.docker.version.data)

    return version
