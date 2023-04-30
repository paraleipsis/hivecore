import asyncio
from asyncio import AbstractEventLoop

from typing import Dict

import faust

from db.broker.stream import TopicStreamHandler
from modules.pubsub.subscriber import Subscriber
from modules.rssh.client.client import ReverseSSHClient
from logger.logs import logger
from node_monitor.config import HOST_MONITOR


class NodeMonitor:
    def __init__(
            self,
            ssh_client: ReverseSSHClient,
            subscriber: Subscriber,
            rssh_host_router: str,
            faust_stream_app: faust.App,
            event_loop: AbstractEventLoop = None
    ):
        self.ssh_client = ssh_client
        self.subscriber = subscriber
        self.rssh_host_router = rssh_host_router
        self.faust_stream_app = faust_stream_app

        if event_loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = event_loop

    async def conn_monitor(self) -> None:
        try:
            while True:
                host_ssh_data = await self.subscriber.get()
                for k, v in HOST_MONITOR.items():
                    if v['active']:
                        asyncio.run_coroutine_threadsafe(
                            coro=self.receiver(
                                ssh_data=host_ssh_data,
                                resource_url=v['url'],
                                kafka_topic=v['kafka_topic'],
                                topic_partitions=int(v['kafka_partitions'])
                            ),
                            loop=self._loop
                        )
        except Exception as exc:
            logger['debug'].debug(
                f'Exception in ssh connections monitoring:\n{str(exc)}'
            )

        return None

    async def receiver(
            self,
            ssh_data: Dict,
            resource_url: str,
            kafka_topic: str,
            topic_partitions: int
    ) -> None:
        try:
            host_ssh_session = ssh_data['session']
            topic_handler = TopicStreamHandler(
                topic=kafka_topic,
                topic_partitions=topic_partitions,
                faust_stream_app=self.faust_stream_app
            )

            async for msg in host_ssh_session.stream(
                    router=self.rssh_host_router,
                    data={
                        'target_resource': resource_url
                    }
            ):
                await topic_handler.send_json_message(
                    key=ssh_data['uuid'],
                    value=msg
                )
        except Exception as exc:
            logger['debug'].debug(
                f'Exception in host data stream:\n{str(exc)}'
            )

        return None

    def run_monitor(self) -> None:
        try:
            asyncio.run_coroutine_threadsafe(
                coro=self.conn_monitor(),
                loop=self._loop
            )
        except Exception as exc:
            logger['debug'].debug(
                f'Error starting Node Monitor:\n{str(exc)}'
            )

        return None
