from typing import Optional, Dict
from uuid import UUID

import asyncssh

from config.server_config import SERVER_URL
from logger.logs import logger
from modules.client.request_handler import ClientRequestHandler
from modules.pubsub.publisher import Publisher
from modules.pubsub.pubsub import pb

_publisher: Optional[Publisher] = None
_connections_channel: Optional[str] = None
_auth_url: Optional[str] = None


def init_publisher() -> None:
    global _publisher

    _publisher = Publisher(pubsub=pb)

    return None


def init_conn_channel(channel: str) -> None:
    global _connections_channel

    _connections_channel = channel

    return None


def init_node_auth_conf(auth_url: str) -> None:
    global _auth_url

    _auth_url = auth_url

    return None


def get_publisher() -> Publisher:
    return _publisher


def get_channel() -> str:
    return _connections_channel


def get_auth_url() -> str:
    return _auth_url


async def publish_host(
        host_uuid: UUID,
        host_connection: asyncssh.SSHClientConnection,
        host_channel: asyncssh.SSHTCPChannel,
        host_session: asyncssh.SSHTCPSession
) -> None:
    msg = {
        'uuid': host_uuid,
        'connection': host_connection,
        'channel': host_channel,
        'session': host_session
    }

    publisher = get_publisher()
    channel = get_channel()

    await publisher.publish(
        channel=channel,
        message=msg
    )

    logger['debug'].debug(
        f"Message published to the channel '{channel}': {msg}"
    )

    return None


async def auth_node(
        node_id: UUID,
        token: str
) -> Dict:
    async with ClientRequestHandler() as client:
        auth_url = get_auth_url()

        node_creds = {
            'node_id': str(node_id),
            'token': token
        }
        response = await client.post_request(
            url=f'{SERVER_URL}/{auth_url}',
            json=node_creds
        )

        data = await response.json()

    return data


async def new_node_conn_handler(
        identify_response: Dict,
        **kwargs
) -> UUID | None:
    node_uuid = UUID(identify_response['response']['node_id'])
    token = identify_response['response']['token']

    auth = await auth_node(
        node_id=node_uuid,
        token=token
    )
    if auth['data']:
        await publish_host(
            host_uuid=node_uuid,
            **kwargs
        )
        return node_uuid

    return None
