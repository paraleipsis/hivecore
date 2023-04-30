from logger.logs import logger
from modules.pubsub.pubsub import pb
from rssh_client.rssh import rssh_client
from modules.pubsub.subscriber import Subscriber
from node_monitor.monitor import NodeMonitor
from core.config import NODE_MONITOR_RSSH_HOST_ROUTER
from db.broker.broker import kafka_event_loop, faust_app


def run_node_monitor() -> None:
    """Run hosts monitoring in a separate thread."""

    sub = Subscriber(pubsub=pb, channel='connections')

    monitor = NodeMonitor(
        rssh_host_router=NODE_MONITOR_RSSH_HOST_ROUTER,
        ssh_client=rssh_client,
        subscriber=sub,
        faust_stream_app=faust_app,
        event_loop=kafka_event_loop
    )

    monitor.run_monitor()

    logger['info'].info(
        f'Node Monitor is running'
    )

    return None
