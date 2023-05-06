from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from docker.crud.crud_snapshots import get_docker_snapshot
from docker.schemas.schemas_plugins import PluginInspectList, PluginInspect
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.utils.docker.utils import get_docker_object_by_id


async def get_all_docker_plugins(
        node_id: UUID,
        session: AsyncSession
) -> PluginInspectList:
    crud_snapshot = await get_docker_snapshot(
        node_id=node_id,
        session=session
    )
    snapshot = DockerSnapshot(**crud_snapshot)
    all_plugins = PluginInspectList(
        plugins=snapshot.docker.plugins.data,
        total=snapshot.docker.plugins.total
    )

    return all_plugins


async def get_docker_plugin(
        node_id: UUID,
        session: AsyncSession,
        plugin_id: str
) -> PluginInspect:
    all_plugins = await get_all_docker_plugins(
        node_id=node_id,
        session=session
    )

    plugin = get_docker_object_by_id(
        object_id=plugin_id,
        docker_object=all_plugins.plugins
    )

    return plugin
