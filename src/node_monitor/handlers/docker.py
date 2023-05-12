import json
from uuid import UUID

from asyncssh import SSHClientConnection

from db.storage_config import DOCKER_PLATFORM_NAME, SWARM_PLATFORM_NAME
from logger.logs import logger
from modules.client.request_handler import ClientRequestHandler
from modules.rssh.client.session import ReverseSSHClientSession
from node_monitor.client.nodes import (update_node_status, create_node_platform_link)
from node_monitor.monitor_config import DOCKER_SNAPSHOT_URL, SNAPSHOT_RSSH_ROUTER
from modules.schemas.schemas_docker_snapshot import DockerSnapshot, SwarmSnapshot
from node_monitor.services.service_node import delete_node_platform_associations, delete_all_node_associations
from node_monitor.services.service_snapshots import save_snapshot


class DockerNodeHandler:
    def __init__(
        self,
        node_uuid: UUID,
        ssh_session: ReverseSSHClientSession,
        ssh_conn: SSHClientConnection,
        snapshot_url: str = DOCKER_SNAPSHOT_URL,
        docker_platform_name: str = DOCKER_PLATFORM_NAME,
        swarm_platform_name: str = SWARM_PLATFORM_NAME,
        docker_topic: str = DOCKER_PLATFORM_NAME,
        swarm_topic: str = SWARM_PLATFORM_NAME,
        snapshot_rssh_router: str = SNAPSHOT_RSSH_ROUTER,
    ):
        self.client = None
        self.docker_platform_name = docker_platform_name
        self.swarm_platform_name = swarm_platform_name
        self.snapshot_url = snapshot_url
        self.docker_topic = docker_topic
        self.swarm_topic = swarm_topic
        self.node_uuid = node_uuid
        self.ssh_session = ssh_session
        self.ssh_conn = ssh_conn
        self.snapshot_rssh_router = snapshot_rssh_router
        self.swarm_state = False

    async def _snapshot_handler(self) -> None:
        try:
            async for snapshot in self.receiver():
                snapshot = json.loads(snapshot['response'])

                snapshot_docker = DockerSnapshot(docker=snapshot[self.docker_platform_name])
                await save_snapshot(
                    client=self.client,
                    kafka_topic=self.docker_topic,
                    platform_name=self.docker_platform_name,
                    node_uuid=self.node_uuid,
                    snapshot=snapshot_docker.dict()
                )

                if snapshot[self.swarm_platform_name] is not None:

                    new_swarm_state = True
                    if new_swarm_state != self.swarm_state:
                        self.swarm_state = new_swarm_state
                        await create_node_platform_link(
                            node_id=self.node_uuid,
                            client=self.client,
                            platform_name=self.swarm_platform_name
                        )

                    snapshot_swarm = SwarmSnapshot(swarm=snapshot[self.swarm_platform_name])
                    await save_snapshot(
                        client=self.client,
                        kafka_topic=self.swarm_topic,
                        platform_name=self.swarm_platform_name,
                        node_uuid=self.node_uuid,
                        snapshot=snapshot_swarm.dict()
                    )

                else:
                    new_swarm_state = False
                    if new_swarm_state != self.swarm_state:
                        self.swarm_state = new_swarm_state
                        await delete_node_platform_associations(
                            node_uuid=self.node_uuid,
                            client=self.client,
                            platform_name=self.swarm_platform_name
                        )

        except Exception as exc:
            logger['debug'].debug(
                f'Exception in host data stream:\n{repr(exc)}'
            )

    async def _on_node_connect(self):
        await update_node_status(
            node_id=self.node_uuid,
            client=self.client,
            active=True
        )

        await create_node_platform_link(
            node_id=self.node_uuid,
            client=self.client,
            platform_name=self.docker_platform_name
        )

    async def _on_node_disconnect(self):
        await update_node_status(
            node_id=self.node_uuid,
            client=self.client,
            active=False
        )

        await delete_all_node_associations(
            client=self.client,
            node_uuid=self.node_uuid
        )

    async def receiver(self):
        async for msg in self.ssh_session.stream(
                router=self.snapshot_rssh_router,
                target_resource=self.snapshot_url
        ):
            yield msg

    async def run_handler(self) -> None:
        async with ClientRequestHandler() as client:
            self.client = client

            try:
                await self._on_node_connect()
            except Exception as exc:
                logger['error'].error(
                    f'Exception updating node Docker data on connection:\n{repr(exc)}'
                )
                self.ssh_conn.close()

                await delete_all_node_associations(
                    client=self.client,
                    node_uuid=self.node_uuid
                )

                return None

            try:
                await self._snapshot_handler()
            finally:
                logger['debug'].debug(
                    f'Stopping node Docker handler. Cleanup DB ...'
                )

                try:
                    self.ssh_conn.close()
                except Exception as exc:
                    logger['debug'].debug(
                        f'Node Monitor: SSH connection already closed'
                    )

                await self._on_node_disconnect()
