import asyncio
from typing import Dict
from uuid import UUID

from modules.client.request_handler import ClientRequestHandler
from node_monitor.client.nodes import (create_or_update_node_snapshot)
from node_monitor.services.service_producer import produce_node_snapshot


async def save_snapshot(
        node_uuid: UUID,
        client: ClientRequestHandler,
        platform_name: str,
        snapshot: Dict,
        kafka_topic: str
) -> None:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            create_or_update_node_snapshot(
                node_id=node_uuid,
                client=client,
                platform_name=platform_name,
                snapshot=snapshot
            )
        )
        tg.create_task(
            produce_node_snapshot(
                node_id=node_uuid,
                topic=kafka_topic,
                new_snapshot=snapshot
            )
        )

    return None
