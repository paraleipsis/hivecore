import asyncio
import gzip
import json
import sys
from asyncio import AbstractEventLoop
from typing import Union, Dict
from uuid import UUID

import asyncssh

from modules.rssh.client.misc import new_node_conn_handler

from modules.rssh.client.session import ReverseSSHClientSession
from logger.logs import logger


class ReverseSSHClient:
    """Object for interacting with the Reverse SSH Client Listener and SSH connections.

       :param local_host:
           The hostname or address to listen on.
       :param local_port:
           The port number to listen on.
       :param client_keys:
           The file that contain an SSH private key for the server to use
           to authenticate itself to the client.
       :param known_hosts: (optional)
           The file that contain a list of trusted client host keys.
       :param reuse_port: (optional)
           Allow this socket to be bound to the same port other
           existing sockets are bound to.
       :param max_packet_size: (optional)
           Maximum allowed network packet size.
    """

    def __init__(
            self,
            local_host: str,
            local_port: int,
            client_keys: str,
            known_hosts: str = None,
            reuse_port: bool = False,
            max_packet_size: int = 32768,
    ):
        self.local_host = local_host
        self.local_port = local_port
        self.client_keys = [client_keys]
        self.known_hosts = known_hosts
        self.reuse_port = reuse_port
        self.max_packet_size = max_packet_size

        self.listener = None

        self._active_connections: Dict[
            UUID, Dict[str, Union[
                asyncssh.SSHTCPChannel,
                asyncssh.SSHTCPSession,
                asyncssh.SSHClientConnection
            ]]
        ] = {}

        self._loop = None

    @property
    def active_connections(self) -> Dict:
        return self._active_connections

    def run_rssh_forever(
            self,
            event_loop: AbstractEventLoop = None
    ) -> None:
        """Run the Reverse SSH Client Listener in the event loop indefinitely until interrupt."""

        try:
            logger['info'].info(
                'Starting Reverse SSH Client forever ...'
            )

            if event_loop is not None:
                self._loop = event_loop
            else:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)

            self._loop.run_until_complete(self.start_listener())
        except (OSError, asyncssh.Error) as exc:
            logger['error'].error(
                f"Error starting client: {str(exc)}"
            )

            sys.exit()

        self._loop.run_forever()

        return None

    async def stop_listener(self):
        logger['info'].info(
            "Shutting down Reverse SSH Client"
        )

        self.disconnect_all()
        self.listener.close()
        await self.listener.wait_closed()

        if self._loop is not None:
            self._loop.stop()
            self._loop.close()

    async def __open_connection(self, conn: asyncssh.SSHClientConnection) -> None:
        """Create a TCP Channel and a TCP Session objects.

           The method sends an identity request to the target host which returns a UUID.

           :class:`SSHTCPChannel`, :class:`SSHTCPSession` and :class:`SSHClientConnection`
           are added to the _active_connections dictionary under the UUID key.

           A message with information about the created connection is sent to
           the :class:`PubSub` 'connections' channel and can be useful for other applications.

           :param conn:
              The :class:`SSHClientConnection` that asyncssh.listen_reverse() method returns.

        """

        logger['debug'].debug(
            'Opening Socket ...'
        )

        try:
            chan, session = await conn.create_connection(
                session_factory=ReverseSSHClientSession,
                remote_host='',
                remote_port=self.local_port,
                max_pktsize=self.max_packet_size
            )

            identification_request = await session._identify()
            # node_uuid = UUID(identification_request['response']['node_id'])

            node_uuid = await new_node_conn_handler(
                identify_response=identification_request,
                host_connection=conn,
                host_channel=chan,
                host_session=session
            )

            if not node_uuid:
                conn.close()
                return None

            self._active_connections[node_uuid] = {
                'connection': conn,
                'channel': chan,
                'session': session
            }

            logger['debug'].debug(
                f"Established connection with host: {node_uuid}"
            )

            await conn.wait_closed()

            del self._active_connections[node_uuid]

            logger['debug'].debug(
                f"Closed connection with host: {node_uuid}"
            )

        except Exception as exc:
            logger['error'].error(
                f"The connection was not established correctly: {repr(exc)}"
            )

            conn.close()

    async def start_listener(self) -> None:
        """Run the Reverse SSH Client Listener.

           After connection with a host create the :class:`SSHClientConnection` object.

        """

        logger['info'].info(
            'Starting Reverse SSH Client ...'
        )

        self.listener = await asyncssh.listen_reverse(
            port=self.local_port,
            client_keys=self.client_keys,
            known_hosts=None,
            reuse_port=True,
            acceptor=self.__open_connection,
        )

    def disconnect(self, host_uuid: UUID) -> None:
        """Close the SSH Channel.

           :param host_uuid:
              The UUID of the host the connection to which should be closed.

        """

        self._active_connections[host_uuid]['connection'].close()

        return None

    def disconnect_all(self) -> None:
        """Close all SSH Channels."""

        for client in self._active_connections.values():
            client['connection'].close()

        return None

    def broadcast(self, message) -> None:
        """Send a message to all SSH channels.

           :param message:
              The object to send.

        """

        for connection in self._active_connections.values():
            connection['channel'].write(gzip.compress(json.dumps(message, separators=(',', ':')).encode('utf-8')))

        return None

    def get_connection(
            self,
            host_uuid: UUID
    ) -> Dict[str, Union[
        asyncssh.SSHTCPChannel,
        asyncssh.SSHTCPSession,
        asyncssh.SSHClientConnection
    ]]:
        connection = self._active_connections[host_uuid]
        return connection
