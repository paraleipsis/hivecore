import asyncio
import json
import uuid
import sys

from typing import MutableMapping, Generator, Optional, Any

import asyncssh
import gzip

from logger.logs import logger


class ReverseSSHClientSession(asyncssh.SSHTCPSession):
    """The :class:`SSHTCPSession` factory object to handle activity on session.

       self._chan :class:`SSHTCPChannel` attribute created after
       the Reverse SSH Client Listener received a connection from remote host
       and called the __open_connection method which in turn called the create_connection method
       which returned this :class:`SSHTCPChannel` object.

       self._requests dictionary attribute created when a connection is established
       and used to store all sent requests by UUID.

    """

    def __init__(self):
        self._chan = None
        self._requests = None

    def connection_made(self, chan: asyncssh.SSHTCPChannel) -> None:
        """Create the _requests dictionary after channel opening."""

        logger['debug'].debug(
            'Session opened'
        )

        self._chan = chan
        self._requests = dict()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        logger['debug'].debug(
            f"Connection lost: {repr(exc)}"
        )

    def session_started(self) -> None:
        logger['debug'].debug(
            'Session successful'
        )

    def data_received(self, data: bytes, datatype: asyncssh.DataType) -> None:
        """Deserializes the received data object and checks
           if the value under the request_id key of data object
           in the _requests attribute, checks if it is in the keys
           of the _requests object.

           Next, writes the received data object under this key of
           _requests object

        """
        data = json.loads(gzip.decompress(data).decode('utf-8'))

        logger['debug'].debug(
            f"Received data: {sys.getsizeof(data)} bytes"
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
            params: Any = None,
            data: Any = None,
            router: str = None,
            **kwargs
    ) -> str:
        """Serializes the data into an object, generates
           a request ID and sends it to the channel.

           :param request_type:
              The HTTP verb: GET, POST, UPDATE, DELETE;
              Data stream: STREAM;
              Host UUID Request: IDENTIFY.
           :param data: (optional)
              The data to send.
           :param params: (optional)
              The query params to send.
           :param router: (optional)
              The endpoint to send the request to.

           :returns: string of request UUID.

        """

        # TODO: remove str conversion for UUID in all methods.
        #  Add pydantic schemas for that (for serialization).

        request = {
            'id': str(uuid.uuid4()),
            'request_type': request_type,
            'router': router,
            'data': data,
            'params': params,
            'kwargs': kwargs
        }

        self._requests[request['id']] = None
        self._chan.write(gzip.compress(json.dumps(request, separators=(',', ':')).encode('utf-8')))

        logger['debug'].debug(
            f"Request '{request_type}' sent to router '{router}'"
        )

        return request['id']

    async def _identify(self, params: MutableMapping = None) -> MutableMapping:
        """The identification request to the target host which returns a UUID.

           :param params: (optional)
              The query params to send.

           :returns: :class:`Dict` with key 'UUID' and value UUID string.

        """

        request_id = self._send_request(
            request_type="IDENTIFY",
            params=params
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as exc:
            logger['error'].error(
                f"Exception in IDENTIFY request: {str(exc)}"
            )
        finally:
            del(self._requests[request_id])

    async def get(
            self,
            router: str,
            params: Any = None,
            **kwargs
    ) -> MutableMapping:
        """Emulates the HTTP GET request.

           :param router:
              The endpoint to send the request to.
           :param params: (optional)
              The query params to send.

           :returns: :class:`Dict` with response data.

        """

        request_id = self._send_request(
            request_type="GET",
            router=router,
            params=params,
            **kwargs
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as exc:
            logger['error'].error(
                f"Exception in GET request: {str(exc)}"
            )
        finally:
            del(self._requests[request_id])

    async def post(
            self,
            router: str,
            data: Any = None,
            params: Any = None,
            **kwargs
    ) -> Generator[MutableMapping, MutableMapping, None]:
        """Emulates the HTTP POST request.

           :param router:
              The endpoint to send the request to.
           :param data: (optional)
              The data to send.
           :param params: (optional)
              The query params to send.

           :returns: :class:`Dict` with response data.

        """

        request_id = self._send_request(
            request_type="POST",
            router=router,
            data=data,
            params=params,
            **kwargs
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as exc:
            logger['error'].error(
                f"Exception in POST request: {str(exc)}"
            )
        finally:
            del (self._requests[request_id])

    async def patch(
            self,
            router: str,
            data: Any = None,
            params: Any = None,
            **kwargs
    ) -> Generator[MutableMapping, MutableMapping, None]:
        """Emulates the HTTP PATCH request.

           :param router:
              The endpoint to send the request to.
           :param data: (optional)
              The data to send.
           :param params: (optional)
              The query params to send.

           :returns: :class:`Dict` with response data.

        """

        request_id = self._send_request(
            request_type="PATCH",
            router=router,
            data=data,
            params=params,
            **kwargs
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as exc:
            logger['error'].error(
                f"Exception in PATCH request: {str(exc)}"
            )
        finally:
            del (self._requests[request_id])

    async def delete(
            self,
            router: str,
            data: Any = None,
            params: Any = None,
            **kwargs
    ) -> Generator[MutableMapping, MutableMapping, None]:
        """Emulates the HTTP DELETE request.

           :param router:
              The endpoint to send the request to.
           :param data: (optional)
              The data to send.
           :param params: (optional)
              The query params to send.

           :returns: :class:`Dict` with response data.

        """

        request_id = self._send_request(
            request_type="DELETE",
            router=router,
            data=data,
            params=params,
            **kwargs
        )

        try:
            while self._requests[request_id] is None:
                await asyncio.sleep(0.1)

            response = self._requests[request_id]

            return response
        except Exception as exc:
            logger['error'].error(
                f"Exception in DELETE request: {str(exc)}"
            )
        finally:
            del (self._requests[request_id])

    async def stream(
            self,
            router: str,
            params: Any = None,
            **kwargs
    ) -> Generator[MutableMapping, MutableMapping, None]:
        """Emulates the HTTP STREAM request.

           :param router:
              The endpoint to send the request to.
           :param params: (optional)
              The query params to send.

           :returns: :class:`Generator` with response data as :class:`Dict`.

        """

        request_id = self._send_request(
            request_type="STREAM",
            router=router,
            params=params,
            **kwargs
        )

        try:
            response_id = 0
            while True:
                while self._requests[request_id] is None:
                    await asyncio.sleep(0.001)

                while self._requests[request_id]['id'] == response_id:
                    await asyncio.sleep(0.001)

                response_id = self._requests[request_id]['id']

                response = self._requests[request_id]

                if response['response'] is None:
                    break

                yield response

            logger['debug'].debug(
                'Closing stream connection'
            )
            del (self._requests[request_id])
        except Exception as exc:
            logger['error'].error(
                f"Exception in STREAM request: {str(exc)}"
            )

            del (self._requests[request_id])
