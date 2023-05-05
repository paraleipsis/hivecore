from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from docker.crud.crud_snapshots import get_docker_snapshot
from docker.schemas.schemas_networks import NetworkInspectList, NetworkInspect
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.utils.docker.utils import get_docker_object_by_id


async def get_all_docker_networks(
        node_id: UUID,
        session: AsyncSession
) -> NetworkInspectList:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    all_networks = NetworkInspectList(
        networks=snapshot.docker.networks.data,
        total=snapshot.docker.networks.total
    )

    return all_networks


async def get_docker_network(
        node_id: UUID,
        session: AsyncSession,
        network_id: str
) -> NetworkInspect:
    all_networks = await get_all_docker_networks(
        node_id=node_id,
        session=session
    )

    network = get_docker_object_by_id(
        object_id=network_id,
        docker_object=all_networks.networks
    )

    return network
