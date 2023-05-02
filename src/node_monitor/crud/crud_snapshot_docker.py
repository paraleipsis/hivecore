from typing import Sequence
from uuid import UUID

from sqlalchemy import select, update, Row, RowMapping, Any, Result
from sqlalchemy.ext.asyncio import AsyncSession

from logger.logs import logger
from modules.exc.exceptions.exceptions_nodes import NoSuchNode
from modules.models import models_nodes


async def get_node_by_id(
    node_id: UUID,
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    query_nodes = select(
        models_nodes.Node
    ).where(
        models_nodes.Node.id == node_id
    )

    result_query_nodes = await session.execute(query_nodes)
    node = result_query_nodes.scalars().first()

    if not node:
        raise NoSuchNode(f'Node with id {node_id} does not exist')

    return node


async def update_node_docker_snapshot_by_id(
    node_id: UUID,
    new_snapshot: str,
    session: AsyncSession
) -> Result:
    query_nodes = update(
        models_nodes.Node
    ).where(
        models_nodes.Node.id == node_id
    ).values(
        snapshot=new_snapshot
    )

    try:
        result = await session.execute(query_nodes)
        await session.commit()
        return result
    except Exception as exc:
        logger['error'].error(
            f"Exception in node update '{node_id}':\n{str(exc)}"
        )
