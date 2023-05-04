import json

from typing import Dict
from uuid import UUID

from db.database.session import async_session_maker
from modules.schemas.schemas_response import GenericResponseModel
from node_monitor.crud.crud_snapshot_docker import get_node_by_id, update_node_docker_snapshot_by_id


async def update_node_docker_snapshot(
        node_id: UUID,
        new_snapshot: Dict,
) -> GenericResponseModel:
    snapshot = json.dumps(new_snapshot)

    async with async_session_maker() as session:
        await update_node_docker_snapshot_by_id(
            node_id=node_id,
            session=session,
            new_snapshot=snapshot
        )
        updated_node = await get_node_by_id(
            node_id=node_id,
            session=session
        )

    return GenericResponseModel(data=updated_node)
