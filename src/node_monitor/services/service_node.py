import asyncio
from uuid import UUID

from modules.client.request_handler import ClientRequestHandler
from node_monitor.client.nodes import (delete_node_snapshot, delete_node_platform_link, delete_all_snapshots,
                                       delete_all_links, delete_all_node_snapshots, delete_all_node_platforms_links)


async def delete_all_associations(
        client: ClientRequestHandler
) -> None:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            delete_all_snapshots(client=client)
        )
        tg.create_task(
            delete_all_links(client=client)
        )

    return None


async def delete_node_platform_associations(
        node_uuid: UUID,
        client: ClientRequestHandler,
        platform_name: str
) -> None:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            delete_node_platform_link(
                node_id=node_uuid,
                client=client,
                platform_name=platform_name
            )
        )
        tg.create_task(
            delete_node_snapshot(
                node_id=node_uuid,
                client=client,
                platform_name=platform_name
            )
        )

    return None


async def delete_all_node_associations(
        node_uuid: UUID,
        client: ClientRequestHandler,
) -> None:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            delete_all_node_platforms_links(
                node_id=node_uuid,
                client=client,
            )
        )
        tg.create_task(
            delete_all_node_snapshots(
                node_id=node_uuid,
                client=client,
            )
        )

    return None
