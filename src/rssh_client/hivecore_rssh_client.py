import asyncio
import logging
import pathlib

from rssh_client.rclient.client import ReverseSSHClient
from config import (SSH_CLIENT_LOCAL_HOST, SSH_CLIENT_LOCAL_PORT, SSH_CLIENT_CLIENT_KEYS,
                    SSH_CLIENT_KNOWN_HOSTS, SSH_CLIENT_REUSE_PORT, SSH_CLIENT_MAX_PACKET_SIZE)

BASE_DIR = pathlib.Path(__file__).parent.parent


def init() -> ReverseSSHClient:
    local_host = SSH_CLIENT_LOCAL_HOST
    local_port = SSH_CLIENT_LOCAL_PORT
    client_keys = SSH_CLIENT_CLIENT_KEYS
    known_hosts = SSH_CLIENT_KNOWN_HOSTS
    reuse_port = SSH_CLIENT_REUSE_PORT
    max_packet_size = SSH_CLIENT_MAX_PACKET_SIZE

    rclient = ReverseSSHClient(
        local_host=local_host,
        local_port=local_port,
        client_keys=client_keys,
        known_hosts=known_hosts,
        reuse_port=reuse_port,
        max_packet_size=max_packet_size
    )

    return rclient


rssh_client = init()


# def main() -> None:
#     logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')
#
#     rssh_client.start()
#
#
# if __name__ == '__main__':
#     main()
