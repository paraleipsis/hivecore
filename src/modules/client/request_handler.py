import json as js_data
from types import TracebackType
from typing import Generator, MutableMapping, Optional, Any, Mapping, Type

import aiohttp
from aiohttp import ClientConnectorError, ClientResponse

from logger.logs import logger
from modules.client.utils import httpize


class ClientRequestHandler:
    def __init__(self):
        self.client_session = aiohttp.ClientSession()

    async def __aenter__(self) -> "ClientRequestHandler":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self.client_session.close()

    async def do_request(
            self,
            url: str,
            method: str,
            params: Optional[Mapping[str, Any]] = None,
            data: Any = None,
            json: Any = None,
    ) -> ClientResponse:
        if data is not None and not isinstance(data, (str, bytes)):
            data = js_data.dumps(data)

        if params is not None:
            params = httpize(params)

        try:
            response = await self.client_session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json
            )

            return response
        except (aiohttp.ClientError, ClientConnectorError, Exception) as exc:
            logger['debug'].debug(
                f"Error {method} request to resource {url}:\n{repr(exc)}"
            )

    async def get_request(
            self,
            url: str,
            **kwargs
    ) -> ClientResponse:
        response = await self.do_request(
            url=url,
            method="GET",
            **kwargs
        )

        return response

    async def post_request(
            self,
            url: str,
            data: Any = None,
            params: Optional[MutableMapping] = None,
            **kwargs
    ) -> ClientResponse:
        response = await self.do_request(
            url=url,
            data=data,
            params=params,
            method="POST",
            **kwargs
        )

        return response

    async def patch_request(
            self,
            url: str,
            data: Any = None,
            params: Optional[MutableMapping] = None,
            **kwargs
    ) -> ClientResponse:
        response = await self.do_request(
            url=url,
            data=data,
            params=params,
            method="PATCH",
            **kwargs
        )

        return response

    async def put_request(
            self,
            url: str,
            data: Any = None,
            params: Optional[MutableMapping] = None,
            **kwargs
    ) -> ClientResponse:
        response = await self.do_request(
            url=url,
            data=data,
            params=params,
            method="PUT",
            **kwargs
        )

        return response

    async def delete_request(
            self,
            url: str,
            data: Any = None,
            params: Optional[MutableMapping] = None,
            **kwargs
    ) -> ClientResponse:
        response = await self.do_request(
            url=url,
            data=data,
            params=params,
            method="DELETE",
            **kwargs
        )

        return response

    async def establish_websocket_conn(
            self,
            url: str,
            **kwargs
    ) -> Generator[MutableMapping, MutableMapping, None]:
        try:
            async with self.client_session.ws_connect(url=url, **kwargs) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        yield msg.data
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        yield None
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        yield None
                        break
        except Exception as exc:
            yield None
            logger['debug'].debug(
                f"Exception in WebSocket connection to resource '{url}':\n{repr(exc)}"
            )
