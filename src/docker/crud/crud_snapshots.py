import json
from typing import Dict

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.exc.exceptions.exceptions_docker import DockerSnapshotDoesNotExist
from modules.exc.exceptions.exceptions_nodes import NoSuchNode
from node_manager.models import models_nodes


async def get_docker_snapshot(
        node_id: UUID,
        session: AsyncSession
) -> Dict:
    query_nodes = select(
        models_nodes.Node
    ).where(
        models_nodes.Node.id == node_id
    )

    result_query_nodes = await session.execute(query_nodes)
    node = result_query_nodes.scalars().first()

    if not node:
        raise NoSuchNode(f'Node with id {node_id} does not exist')

    snapshot = node.docker_snapshot

    if not snapshot:
        raise DockerSnapshotDoesNotExist(f"Docker snapshot for Node '{node_id}' does not exist")

    deserialized_snapshot = json.loads(snapshot)

    return deserialized_snapshot
