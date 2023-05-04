import asyncio
import json
from asyncio import AbstractEventLoop

from typing import Dict

from db.broker.broker import produce
from modules.pubsub.subscriber import Subscriber
from modules.rssh.client.client import ReverseSSHClient
from logger.logs import logger
from node_monitor.config import HOST_MONITOR
from node_monitor.services.service_snapshot_docker import update_node_docker_snapshot


class NodeMonitor:
    def __init__(
            self,
            ssh_client: ReverseSSHClient,
            subscriber: Subscriber,
            rssh_host_router: str,
            event_loop: AbstractEventLoop = None
    ):
        self.ssh_client = ssh_client
        self.subscriber = subscriber
        self.rssh_host_router = rssh_host_router

        if event_loop is None:
            self._loop = asyncio.get_running_loop()
        else:
            self._loop = event_loop

    async def _conn_monitor(self) -> None:
        try:
            while True:
                host_ssh_data = await self.subscriber.get()
                for v in HOST_MONITOR.values():
                    if v['active']:
                        asyncio.run_coroutine_threadsafe(
                            coro=self._receiver(
                                ssh_data=host_ssh_data,
                                resource_url=v['url'],
                                kafka_topic=v['kafka_topic'],
                            ),
                            loop=self._loop
                        )
        except Exception as exc:
            logger['debug'].debug(
                f'Exception in ssh connections monitoring:\n{str(exc)}'
            )

        return None

    async def _receiver(
            self,
            ssh_data: Dict,
            resource_url: str,
            kafka_topic: str,
    ) -> None:
        try:
            host_ssh_session = ssh_data['session']

            async for msg in host_ssh_session.stream(
                    router=self.rssh_host_router,
                    target_resource=resource_url
            ):
                snapshot = json.loads(msg['response'])

                await update_node_docker_snapshot(
                    node_id=ssh_data['uuid'],
                    new_snapshot=snapshot
                )

                await produce(
                    topic=kafka_topic,
                    key=str(ssh_data['uuid']),
                    value=snapshot
                )
        except Exception as exc:
            logger['debug'].debug(
                f'Exception in host data stream:\n{str(exc)}'
            )

        return None

    def run_monitor(self) -> None:
        try:
            asyncio.run_coroutine_threadsafe(
                coro=self._conn_monitor(),
                loop=self._loop
            )
        except Exception as exc:
            logger['debug'].debug(
                f'Error starting Node Monitor:\n{str(exc)}'
            )

        return None
