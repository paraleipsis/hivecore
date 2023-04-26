from modules.rssh.client.client import ReverseSSHClient
from rssh_client.config import (SSH_CLIENT_LOCAL_HOST, SSH_CLIENT_LOCAL_PORT, SSH_CLIENT_CLIENT_KEYS,
                                SSH_CLIENT_KNOWN_HOSTS, SSH_CLIENT_REUSE_PORT, SSH_CLIENT_MAX_PACKET_SIZE)
from modules.pubsub.publisher import Publisher
from modules.pubsub.pubsub import pb


def init_rssh_client() -> ReverseSSHClient:
    rclient = ReverseSSHClient(
        local_host=SSH_CLIENT_LOCAL_HOST,
        local_port=SSH_CLIENT_LOCAL_PORT,
        client_keys=SSH_CLIENT_CLIENT_KEYS,
        known_hosts=SSH_CLIENT_KNOWN_HOSTS,
        reuse_port=SSH_CLIENT_REUSE_PORT,
        max_packet_size=SSH_CLIENT_MAX_PACKET_SIZE,
        publisher=Publisher(pubsub=pb),
        pubsub_channel='connections'
    )

    return rclient


rssh_client = init_rssh_client()
