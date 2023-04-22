import asyncio
import gzip
import json
import uuid
from typing import MutableMapping, Tuple

import asyncssh
import traceback

from logger.logs import logger


class ReverseSSHServerSession(asyncssh.SSHTCPSession):
    def __init__(
            self,
            callbacks: MutableMapping,
            request_types: Tuple,
            stream_types: Tuple,
            internal_request_types: Tuple,
            server_uuid: uuid.UUID = None
    ):
        self._callbacks = callbacks
        self.request_types = request_types
        self.stream_types = stream_types
        self.internal_request_types = internal_request_types
        self._chan = None
        self._loop = asyncio.get_event_loop()
        self._server_uuid = server_uuid

    def connection_made(self, chan: asyncssh.SSHTCPChannel) -> None:
        """New connection established"""

        # logging.debug("Connection incoming")
        logger['debug'].debug(
            f'Connection incoming ...'
        )
        self._chan = chan

    def connection_lost(self, exc: Exception) -> None:
        """Lost the connection to the client"""

        # logging.debug(f"Connection lost\n{exc}")
        logger['debug'].debug(
            f"Connection lost\n{exc}"
        )

    def session_started(self) -> None:
        """New session established successfully"""

        # logging.debug("Connection successful")
        logger['debug'].debug(
            f"Connection successful"
        )

    def data_received(self, data: bytes, datatype: asyncssh.DataType) -> None:
        """New data coming in"""

        # logging.debug(f"Received data: {data}")
        logger['debug'].debug(
            f"Received data: {json.loads(gzip.decompress(data).decode('utf-8'))}"
        )
        self._dispatch(data)

    def eof_received(self) -> None:
        """Got an EOF, close the channel"""

        # logging.debug("EOF")
        logger['debug'].debug(
            f"EOF"
        )
        self._chan.exit(0)

    def _dispatch(self, data: bytes) -> None:
        try:
            request = json.loads(gzip.decompress(data).decode('utf-8'))

            if 'id' not in request:
                logger['debug'].debug(
                    "Malformed request: missing 'id'"
                )
                self._send_response(0, 400, {"message": "Missing 'id'"})

            if 'request_type' not in request:
                logger['debug'].debug(
                    "Malformed request: missing 'request_type'"
                )
                self._send_response(request['id'], 400, {"message": "Missing 'request_type'"})

            if 'router' not in request:
                logger['debug'].debug(
                    "Malformed request: missing 'router'"
                )
                self._send_response(request['id'], 400, {"message": "Missing 'router'"})

            if request['request_type'] == 'POST' and 'data' not in request['request']:
                logger['debug'].debug(
                    "Malformed request: missing 'data'"
                )
                self._send_response(request['id'], 400, {"message": "Missing 'data'"})

            elif request['request_type'] == 'UPDATE' and 'data' not in request['request']:
                logger['debug'].debug(
                    "Malformed request: missing 'data'"
                )
                self._send_response(request['id'], 400, {"message": "Missing 'data'"})

            if request['request_type'] in self.stream_types:
                asyncio.run_coroutine_threadsafe(self.__process_stream(request), self._loop)
                return None

            if request['request_type'] in self.internal_request_types:
                asyncio.run_coroutine_threadsafe(self.__process_internal_request(request), self._loop)
                return None

            asyncio.run_coroutine_threadsafe(self.__process_request(request), self._loop)
            return None

        except Exception as exc:
            logger['error'].error(
                f"Unable to process request: {exc}"
            )
            self._send_response(0, 400, {"message": "Unable to process request"})
            return None

    async def __process_internal_request(self, request: MutableMapping) -> None:
        response = None

        if request['request_type'] == 'IDENTIFY':
            if self._server_uuid is None:
                self._server_uuid = uuid.uuid4()
            response = {'UUID': str(self._server_uuid)}

        try:
            self._send_response(
                request_id=request['id'],
                ssh_response_code=200,
                response=response
            )

            return None

        except Exception as exc:
            logger['error'].error(
                f"Internal error when executing {request['request_type']}\n{str(exc)}"
            )
            self._send_response(request['id'], 500, {"message": str(exc), "traceback": traceback.format_exc()})
            return None

    async def __process_request(self, request: MutableMapping) -> None:
        if request['request_type'] not in self._callbacks:
            logger['debug'].debug(
                f"No callback found for {request['request_type']}"
            )
            self._send_response(request['id'], 404)
            return None

        if request['router'] not in self._callbacks[request['request_type']]:
            logger['debug'].debug(
                f"No callback found for {request['request_type']} on {request['router']}"
            )
            self._send_response(request['id'], 404)
            return None

        callback = self._callbacks[request['request_type']][request['router']]

        prepared_request = request['data']

        try:
            if prepared_request is None:
                response = await callback()
            else:
                response = await callback(**prepared_request)

            self._send_response(
                request_id=request['id'],
                ssh_response_code=200,
                response=response
            )

            return None

        except Exception as exc:
            logger['error'].error(
                f"Internal error when executing {request['request_type']} on {request['resource']}\n{str(exc)}"
            )
            self._send_response(request['id'], 500, {"message": str(exc), "traceback": traceback.format_exc()})
            return None

    async def __process_stream(self, request: MutableMapping) -> None:
        if request['request_type'] not in self._callbacks:
            logger['debug'].debug(
                f"No request type found for {request['request_type']}"
            )
            self._send_response(request['id'], 404)
            return

        if request['router'] not in self._callbacks[request['request_type']]:
            logger['debug'].debug(
                f"No callback found for {request['request_type']} on {request['router']}"
            )
            self._send_response(request['id'], 404)
            return

        callback = self._callbacks[request['request_type']][request['router']]

        prepared_request = request['data']

        # TODO: fix this ugly stuff
        if prepared_request is None:
            prepared_request = {}

        try:
            async for response in callback(**prepared_request):
                self._send_response(
                    request_id=request['id'],
                    ssh_response_code=200,
                    response=response
                )
            return None

        except Exception as exc:
            logger['error'].error(
                f"Internal error when executing {request['request_type']} on {request['resource']}\n{str(exc)}"
            )
            self._send_response(request['id'], 500, {"message": str(exc), "traceback": traceback.format_exc()})

    def _send_response(
            self,
            request_id: float,
            ssh_response_code: int,
            response: MutableMapping = None
    ) -> None:
        """Send a response to the given client request"""

        ssh_response = {
            'id': str(uuid.uuid4()),
            'request_id': request_id,
            'ssh_response_code': ssh_response_code,
            'response': response
        }

        logger['info'].info(
            f"{ssh_response_code} response to {request_id}"
        )
        self._chan.write(gzip.compress(json.dumps(ssh_response, separators=(',', ':')).encode('utf-8')))
        return None
