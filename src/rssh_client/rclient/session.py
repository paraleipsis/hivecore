import json
import uuid
from typing import MutableMapping

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

    def connection_lost(self, exc: Exception) -> None:
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

    def send_request(
            self,
            router: str,
            target_resource: str,
            request_type: str,
            data: MutableMapping
    ) -> str:

        request = {
            'id': str(uuid.uuid4()),
            'request_type': request_type,
            'router': router,
            'target_resource': target_resource,
            'data': data
        }

        self._requests[request['id']] = None
        self._chan.write(gzip.compress(json.dumps(request, separators=(',', ':')).encode('utf-8')))
        logging.debug(f"Request '{request_type}' sent to '{router}' with param '{target_resource}' and data '{data}'")

        return request['id']
