import asyncio
import json
import uuid
from typing import MutableMapping, Generator, Optional

import asyncssh
import gzip
import logging


class ReverseSSHClientSession(asyncssh.SSHTCPSession):
    def __init__(self):
        self._chan = None
        self._requests = None

    def connection_made(self, chan: asyncssh.SSHTCPChannel) -> None:
        logging.debug("Session opened")

        self._chan = chan
        self._requests = dict()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        logging.debug(f"Connection lost: {exc}")

    def session_started(self) -> None:
        logging.debug("Session successful")

    def data_received(self, data: bytes, datatype: asyncssh.DataType) -> None:
        logging.debug(f"Received data: {data}")

        try:
            data = json.loads(gzip.decompress(data).decode('utf-8'))

            if data['request_id'] in self._requests:
                if callable(self._requests[data['request_id']]):
                    self._requests[data['request_id']](data)

                self._requests[data['request_id']] = data

        except Exception as e:
            logging.exception(f"There was an error processing the server response: {e}")

    def eof_received(self) -> None:
        logging.debug("Received EOF")
        self._chan.exit(0)

    def _send_request(
            self,
            router: str,
            request_type: str,
            data: MutableMapping,
    ) -> str:

        # TODO: remove str conversion for UUID in all methods.
        #  Add pydantic schemas for that (for serialization).

        request = {
            'id': str(uuid.uuid4()),
            'request_type': request_type,
            'router': router,
            'data': data,
        }

        self._requests[request['id']] = None
        self._chan.write(gzip.compress(json.dumps(request, separators=(',', ':')).encode('utf-8')))
        logging.debug(f"Request '{request_type}' sent to '{router}' with data '{data}'")

        return request['id']

    async def get(
            self,
            router: str,
            data: MutableMapping = None,
    ) -> MutableMapping:

        request_id = self._send_request(
            request_type="GET",
            router=router,
            data=data,
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del(self._requests[request_id])

    async def post(
            self,
            router: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._send_request(
            request_type="POST",
            router=router,
            data=data
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del (self._requests[request_id])

    async def update(
            self,
            router: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._send_request(
            request_type="UPDATE",
            router=router,
            data=data
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del (self._requests[request_id])

    async def delete(
            self,
            router: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._send_request(
            request_type="DELETE",
            router=router,
            data=data
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as e:
            logging.debug(f"Exception in get request: {e}")
        finally:
            del (self._requests[request_id])

    async def ws(
            self,
            router: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._send_request(
            request_type="WS",
            router=router,
            data=data,
        )

        try:
            response_id = 0
            while True:
                while self._requests[request_id] is None:
                    await asyncio.sleep(0.1)

                if self._requests[request_id]['id'] == response_id:
                    await asyncio.sleep(0.1)

                response_id = self._requests[request_id]['id']

                response = self._requests[request_id]

                yield response
        except Exception as e:
            logging.debug(f"Exception in ws connection: {e}")
        finally:
            logging.debug("Closing ws connection")
            del (self._requests[request_id])
