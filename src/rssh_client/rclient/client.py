import asyncio
import logging
import sys
import time
from typing import MutableMapping, Generator

import asyncssh
from asyncssh import SSHClientConnectionOptions

from rssh_client.rclient.session import ReverseSSHClientSession


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

        self._session = None
        self._loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self._loop)

    def start(self):
        try:
            self._loop.run_until_complete(self.__listen())
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Error starting client: ' + str(exc))

        self._loop.run_forever()

    async def __open_connection(self, conn: asyncssh.SSHClientConnection) -> None:
        logging.debug("Opening Socket")

        chan, self._session = await conn.create_connection(
            session_factory=ReverseSSHClientSession,
            remote_host='',
            remote_port=int(self.local_port)
        )

    async def __listen(self) -> None:
        try:
            await asyncssh.listen_reverse(
                port=int(self.local_port),
                client_keys=self.client_keys,
                known_hosts=None,
                reuse_port=True,
                options=SSHClientConnectionOptions(max_pktsize=self.max_packet_size),
                acceptor=self.__open_connection
            )
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Error starting client: ' + str(exc))

    async def get(
            self,
            router: str,
            target_resource: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._session.send_request(
            request_type="GET",
            router=router,
            target_resource=target_resource,
            data=data
        )

        try:
            while self._session._requests[request_id] is None:
                time.sleep(0.1)

            response = self._session._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del(self._session._requests[request_id])

    def post(
            self,
            router: str,
            target_resource: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._session.send_request(
            request_type="POST",
            router=router,
            target_resource=target_resource,
            data=data
        )

        try:
            while self._session._requests[request_id] is None:
                time.sleep(0.1)

            response = self._session._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del (self._session._requests[request_id])

    def update(
            self,
            router: str,
            target_resource: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._session.send_request(
            request_type="UPDATE",
            router=router,
            target_resource=target_resource,
            data=data
        )

        try:
            while self._session._requests[request_id] is None:
                time.sleep(0.1)

            response = self._session._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del (self._session._requests[request_id])

    def delete(
            self,
            router: str,
            target_resource: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._session.send_request(
            request_type="DELETE",
            router=router,
            target_resource=target_resource,
            data=data
        )

        try:
            while self._session._requests[request_id] is None:
                time.sleep(0.1)

            response = self._session._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del (self._session._requests[request_id])

    async def ws(
            self,
            router: str,
            target_resource: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._session.send_request(
            request_type="WS",
            router=router,
            target_resource=target_resource,
            data=data,
        )

        try:
            response_id = 0
            while True:
                while self._session._requests[request_id] is None:
                    time.sleep(0.1)

                if self._session._requests[request_id]['id'] == response_id:
                    continue

                response_id = self._session._requests[request_id]['id']

                response = self._session._requests[request_id]

                yield response
        except Exception as e:
            logging.debug(f"Exception in ws connection: {e}")
        finally:
            logging.debug("Closing ws connection")
            del (self._session._requests[request_id])
