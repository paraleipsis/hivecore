from typing import MutableMapping, Mapping
from uuid import UUID

from config.server_config import SERVER_URL
from logger.logs import logger
from modules.client.request_handler import ClientRequestHandler
from modules.exc.exceptions.exceptions_nodes import PlatformNodeLinkError, NodeStatusError, NodeSnapshotError
from node_monitor.monitor_config import (NODES_URL, NODE_STATUS_URL, NODE_PLATFORM_URL, NODE_SNAPSHOT_URL)


async def update_node_status(
        node_id: UUID,
        active: bool,
        client: ClientRequestHandler
) -> MutableMapping:
    params = {
        'new_status': active
    }

    response = await client.patch_request(
        url=f'{SERVER_URL}/{NODES_URL}/{node_id}/{NODE_STATUS_URL}',
        params=params
    )

    if response.status != 200:
        logger['error'].error(
            f'Error updating node status: {response.status} {response}'
        )
        raise NodeStatusError

    data = await response.json()

    return data


async def create_node_platform_link(
        node_id: UUID,
        platform_name: str,
        client: ClientRequestHandler
) -> MutableMapping:
    params = {
        'platform_name': platform_name
    }

    response = await client.post_request(
        url=f'{SERVER_URL}/{NODES_URL}/{node_id}/{NODE_PLATFORM_URL}',
        params=params
    )

    if response.status != 200:
        logger['error'].error(
            f'Error creating node-platform link: {response.status} {response}'
        )
        raise PlatformNodeLinkError

    data = await response.json()

    return data


async def delete_node_platform_link(
        node_id: UUID,
        platform_name: str,
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.delete_request(
        url=f'{SERVER_URL}/{NODES_URL}/{node_id}/{NODE_PLATFORM_URL}/{platform_name}'
    )

    if response.status != 200:
        logger['error'].error(
            f'Error deleting node-platform link: {response.status} {response}'
        )
        raise PlatformNodeLinkError

    data = await response.json()

    return data


async def create_or_update_node_snapshot(
        node_id: UUID,
        platform_name: str,
        snapshot: Mapping,
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.put_request(
        url=f'{SERVER_URL}/{NODES_URL}/{node_id}/{NODE_SNAPSHOT_URL}/{platform_name}',
        json=snapshot
    )

    if response.status != 200:
        logger['error'].error(
            f'Error creating node-platform snapshot: {response.status} {response}'
        )
        raise NodeSnapshotError

    data = await response.json()

    return data


async def delete_node_snapshot(
        node_id: UUID,
        platform_name: str,
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.delete_request(
        url=f'{SERVER_URL}/{NODES_URL}/{node_id}/{NODE_SNAPSHOT_URL}/{platform_name}'
    )

    if response.status != 200:
        logger['error'].error(
            f'Error deleting node-platform snapshot: {response.status} {response}'
        )
        raise NodeSnapshotError

    data = await response.json()

    return data


async def delete_all_node_snapshots(
        node_id: UUID,
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.delete_request(
        url=f'{SERVER_URL}/{NODES_URL}/{node_id}/{NODE_SNAPSHOT_URL}'
    )

    if response.status != 200:
        logger['error'].error(
            f'Error deleting node-platform snapshot: {response.status} {response}'
        )
        raise NodeSnapshotError

    data = await response.json()

    return data


async def delete_all_node_platforms_links(
        node_id: UUID,
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.delete_request(
        url=f'{SERVER_URL}/{NODES_URL}/{node_id}/{NODE_PLATFORM_URL}'
    )

    if response.status != 200:
        logger['error'].error(
            f'Error deleting node-platform snapshot: {response.status} {response}'
        )
        raise NodeSnapshotError

    data = await response.json()

    return data


async def delete_all_snapshots(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.delete_request(
        url=f'{SERVER_URL}/{NODES_URL}/{NODE_SNAPSHOT_URL}'
    )

    if response.status != 200:
        logger['error'].error(
            f'Error deleting node-platform snapshot: {response.status} {response}'
        )
        raise NodeSnapshotError

    data = await response.json()

    return data


async def delete_all_links(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.delete_request(
        url=f'{SERVER_URL}/{NODES_URL}/{NODE_PLATFORM_URL}'
    )

    if response.status != 200:
        logger['error'].error(
            f'Error deleting node-platform snapshot: {response.status} {response}'
        )
        raise NodeSnapshotError

    data = await response.json()

    return data
