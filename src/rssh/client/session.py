import asyncio
import json
import uuid
from typing import MutableMapping, Generator, Optional

import asyncssh
import gzip

from logger.logs import logger


class ReverseSSHClientSession(asyncssh.SSHTCPSession):
    def __init__(self):
        self._chan = None
        self._requests = None

    def connection_made(self, chan: asyncssh.SSHTCPChannel) -> None:
        logger['debug'].debug(
            'Session opened'
        )

        self._chan = chan
        self._requests = dict()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        logger['debug'].debug(
            f"Connection lost: {exc}"
        )

    def session_started(self) -> None:
        logger['debug'].debug(
            'Session successful'
        )

    def data_received(self, data: bytes, datatype: asyncssh.DataType) -> None:
        data = json.loads(gzip.decompress(data).decode('utf-8'))

        logger['debug'].debug(
            f"Received data: {data}"
        )

        try:
            if data['request_id'] in self._requests:
                if callable(self._requests[data['request_id']]):
                    self._requests[data['request_id']](data)

                self._requests[data['request_id']] = data

        except Exception as exc:
            logger['error'].error(
                f"There was an error processing the server response: {str(exc)}"
            )

    def eof_received(self) -> None:
        logger['debug'].debug(
            "Received EOF"
        )

        self._chan.exit(0)

    def _send_request(
            self,
            request_type: str,
            data: MutableMapping = None,
            router: str = None,
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

        logger['debug'].debug(
            f"Request '{request_type}' sent to '{router}' with data '{data}'"
        )

        return request['id']

    async def _identify(
            self,
            data: MutableMapping = None,
    ) -> MutableMapping:

        request_id = self._send_request(
            request_type="IDENTIFY",
            data=data,
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as exc:
            logger['error'].error(
                f"Exception in get request: {str(exc)}"
            )
        finally:
            del(self._requests[request_id])

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
        except Exception as exc:
            logger['error'].error(
                f"Exception in get request: {str(exc)}"
            )
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
        except Exception as exc:
            logger['error'].error(
                f"Exception in post request: {str(exc)}"
            )
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
        except Exception as exc:
            logger['error'].error(
                f"Exception in update request: {str(exc)}"
            )
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
        except Exception as exc:
            logger['error'].error(
                f"Exception in delete request: {str(exc)}"
            )
        finally:
            del (self._requests[request_id])

    async def stream(
            self,
            router: str,
            data: MutableMapping = None
    ) -> Generator[MutableMapping, MutableMapping, None]:

        request_id = self._send_request(
            request_type="STREAM",
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
        except Exception as exc:
            logger['error'].error(
                f"Exception in stream request: {str(exc)}"
            )
        finally:
            logger['debug'].debug(
                'Closing stream connection'
            )
            del (self._requests[request_id])
