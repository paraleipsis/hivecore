import asyncio
import gzip
import json
import sys
from typing import MutableMapping, Union
from uuid import UUID

import asyncssh
from asyncssh import SSHClientConnectionOptions, SSHTCPSession, SSHTCPChannel

from rssh.client.session import ReverseSSHClientSession
from logger.logs import logger


class ReverseSSHClient:
    def __init__(
            self,
            local_host: str,
            local_port: int,
            client_keys: str,
            known_hosts: str = None,
            reuse_port: bool = False,
            max_packet_size: int = 32768
    ):
        self.local_host = local_host
        self.local_port = local_port
        self.client_keys = [client_keys]
        self.known_hosts = known_hosts
        self.reuse_port = reuse_port
        self.max_packet_size = max_packet_size

        self.active_connections: MutableMapping[UUID, MutableMapping[str, Union[SSHTCPChannel, SSHTCPSession]]] = {}
        self._loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self._loop)

    def start(self):
        try:
            self._loop.run_until_complete(self.__listen())
        except (OSError, asyncssh.Error) as exc:
            logger['error'].error(
                f"Error starting client: {str(exc)}"
            )
            sys.exit()

        self._loop.run_forever()

    async def __open_connection(self, conn: asyncssh.SSHClientConnection) -> None:
        logger['debug'].debug(
            'Opening Socket ...'
        )

        try:
            chan, session = await conn.create_connection(
                session_factory=ReverseSSHClientSession,
                remote_host='',
                remote_port=int(self.local_port)
            )

            identification_request = await session.get(router='/identification')

            # TODO: Add check for agent Token and UUID in PostgreSQL database. UUID and Token need to be generated on
            #  the main server in the node_manager application. Then UUID and Token pass as environment variables to
            #  the node agent on deployment. For each next request we need to pass in required method a specific
            #  session (by a host UUID as Path param)

            uuid = identification_request['response']

            self.active_connections[uuid] = {
                'connection': conn,
                'channel': chan,
                'session': session
            }

            logger['debug'].debug(
                f"Established connection with host: {uuid}"
            )

            await conn.wait_closed()

            del self.active_connections[uuid]

            logger['debug'].debug(
                f"Closed connection with host: {uuid}"
            )

        except Exception as exc:
            logger['error'].error(
                f"The connection was not established correctly: {str(exc)}"
            )

    async def __listen(self) -> None:
        await asyncssh.listen_reverse(
            port=int(self.local_port),
            client_keys=self.client_keys,
            known_hosts=None,
            reuse_port=True,
            options=SSHClientConnectionOptions(max_pktsize=self.max_packet_size),
            acceptor=self.__open_connection
        )

    def disconnect(self, host_uuid: UUID) -> None:
        self.active_connections[host_uuid]['connection'].close()

        return None

    def broadcast(self, message: str):
        for connection in self.active_connections.values():
            connection['channel'].write(gzip.compress(json.dumps(message, separators=(',', ':')).encode('utf-8')))
