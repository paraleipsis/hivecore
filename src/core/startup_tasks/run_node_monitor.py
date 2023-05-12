from typing import Optional

from logger.logs import logger
from modules.pubsub.pubsub import pb
from rssh_client.rssh import get_rssh_client
from modules.pubsub.subscriber import Subscriber
from node_monitor.monitor import NodeMonitor
from db.broker.broker import get_kafka_loop

_monitor: Optional[NodeMonitor] = None


def get_node_monitor():
    return _monitor


def run_node_monitor() -> NodeMonitor:
    """Run hosts monitoring in a separate thread."""

    global _monitor

    sub = Subscriber(pubsub=pb, channel='connections')

    _monitor = NodeMonitor(
        ssh_client=get_rssh_client(),
        subscriber=sub,
        event_loop=get_kafka_loop()
    )

    _monitor.run_monitor()

    logger['info'].info(
        f'Node Monitor is running'
    )

    return _monitor
