import asyncio
from asyncio import AbstractEventLoop

from typing import Dict

from asyncssh import SSHTCPSession

from modules.client.request_handler import ClientRequestHandler
from modules.pubsub.subscriber import Subscriber
from modules.rssh.client.client import ReverseSSHClient
from logger.logs import logger
from node_monitor.monitor_config import (ACTIVE_PLATFORMS_URL, ACTIVE_PLATFORMS_RSSH_ROUTER)
from node_monitor.handlers.docker import DockerNodeHandler
from node_monitor.services.service_node import delete_all_associations


class NodeMonitor:
    def __init__(
            self,
            ssh_client: ReverseSSHClient,
            subscriber: Subscriber,
            event_loop: AbstractEventLoop = None,
            active_platforms_url: str = ACTIVE_PLATFORMS_URL,
            active_platforms_rssh_router: str = ACTIVE_PLATFORMS_RSSH_ROUTER,
    ):
        self.ssh_client = ssh_client
        self.subscriber = subscriber
        self.active_platforms_url = active_platforms_url
        self.active_platforms_rssh_router = active_platforms_rssh_router
        self.platforms_handlers = {
            'docker': DockerNodeHandler
        }

        if event_loop is None:
            self._loop = asyncio.get_running_loop()
        else:
            self._loop = event_loop

        self.monitor_task = None

    async def _conn_monitor(self) -> None:
        try:
            while True:
                host_ssh_data = await self.subscriber.get()
                host_active_platforms = await self.get_active_platforms(
                    ssh_session=host_ssh_data['session']
                )
                await self._run_node_handlers(
                    node_uuid=host_ssh_data['uuid'],
                    ssh_session=host_ssh_data['session'],
                    ssh_conn=host_ssh_data['connection'],
                    active_platforms=host_active_platforms['data']
                )
        except Exception as exc:
            logger['error'].error(
                f'Error monitoring ssh connections:\n{str(exc)}'
            )

        return None

    async def _run_node_handlers(
            self,
            active_platforms: Dict[str, bool],
            **ssh_params
    ):
        for platform in active_platforms:
            try:
                handler = self.platforms_handlers[platform]
                handler_instance = handler(**ssh_params)
                asyncio.run_coroutine_threadsafe(
                    coro=handler_instance.run_handler(),
                    loop=self._loop
                )
            except Exception as exc:
                logger['error'].error(
                    f'Error starting {platform} receiver:\n{repr(exc)}'
                )

    async def get_active_platforms(
            self,
            ssh_session: SSHTCPSession
    ) -> Dict:
        active_platforms = await ssh_session.get(
            router=self.active_platforms_rssh_router,
            target_resource=self.active_platforms_url
        )

        return active_platforms['response']

    def run_monitor(self) -> None:
        try:
            self.monitor_task = asyncio.run_coroutine_threadsafe(
                coro=self._conn_monitor(),
                loop=self._loop
            )
        except Exception as exc:
            logger['debug'].debug(
                f'Error starting Node Monitor:\n{repr(exc)}'
            )

        return None

    @staticmethod
    async def cleanup():
        async with ClientRequestHandler() as client:
            await delete_all_associations(client=client)

    async def stop_monitor(self):
        logger['debug'].debug(
            f'Closing Node Monitor ...'
        )

        await self.cleanup()
        self.monitor_task.cancel()
