from typing import Dict
from uuid import UUID

from db.broker.broker import produce


async def produce_node_snapshot(
        node_id: UUID,
        topic: str,
        new_snapshot: Dict,
) -> None:
    await produce(
        topic=topic,
        key=str(node_id),
        value=new_snapshot
    )

    return None
