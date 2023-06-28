import json
from typing import Dict

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.exc.exceptions.exceptions_docker import DockerSnapshotDoesNotExist
from modules.exc.exceptions.exceptions_nodes import NodeSnapshotError
from node_manager.models import models_snapshots


async def get_docker_snapshot(
        node_id: UUID,
        session: AsyncSession
) -> Dict:
    query_snapshot = select(
        models_snapshots.Snapshot
    ).where(
        models_snapshots.Snapshot.node_id == node_id,
        models_snapshots.Snapshot.platform_name == 'docker'
    )

    result_query_snapshots = await session.execute(query_snapshot)
    snapshot = result_query_snapshots.scalars().first()

    if not snapshot:
        raise NodeSnapshotError(f"No snapshot for node '{node_id}'")

    snapshot_json = snapshot.snapshot

    deserialized_snapshot = json.loads(snapshot_json)

    return deserialized_snapshot
