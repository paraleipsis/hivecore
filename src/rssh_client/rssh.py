from typing import Optional, Dict

from modules.rssh.client.client import ReverseSSHClient
from modules.rssh.client.misc import init_publisher, init_conn_channel, init_node_auth_conf
from rssh_client.rssh_config import (SSH_CLIENT_LOCAL_HOST, SSH_CLIENT_LOCAL_PORT, SSH_CLIENT_PRIVATE_KEY_PATH,
                                     SSH_CLIENT_KNOWN_HOSTS, SSH_CLIENT_REUSE_PORT, SSH_CLIENT_MAX_PACKET_SIZE,
                                     NODE_AUTH_URL)


_rssh_client: Optional[ReverseSSHClient] = None


def init_rssh_client() -> ReverseSSHClient:
    """Initializes the :class:`ReverseSSHClient` object with
       specific configuration. Loads all environment variables.

       :returns: :class:`ReverseSSHClient`.

    """

    global _rssh_client

    init_publisher()
    init_conn_channel(channel='connections')
    init_node_auth_conf(auth_url=NODE_AUTH_URL)

    _rssh_client = ReverseSSHClient(
        local_host=SSH_CLIENT_LOCAL_HOST,
        local_port=SSH_CLIENT_LOCAL_PORT,
        client_keys=SSH_CLIENT_PRIVATE_KEY_PATH,
        known_hosts=SSH_CLIENT_KNOWN_HOSTS,
        reuse_port=SSH_CLIENT_REUSE_PORT,
        max_packet_size=SSH_CLIENT_MAX_PACKET_SIZE,
    )

    return _rssh_client


def get_rssh_client() -> ReverseSSHClient:
    return _rssh_client


def get_active_connections() -> Dict:
    return _rssh_client.active_connections
