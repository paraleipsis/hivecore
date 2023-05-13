import asyncio

from rssh_client.rssh import get_rssh_client
from rssh_client.rssh_config import SSH_CLIENT_LOCAL_HOST, SSH_CLIENT_LOCAL_PORT
from logger.logs import logger


def run_rssh_client() -> None:
    """Run the Reverse SSH Client Listener in a separate thread."""

    rssh_client = get_rssh_client()
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(
        coro=rssh_client.start_listener(),
        loop=loop
    )

    logger['info'].info(
        f'Reverse SSH Client running on {SSH_CLIENT_LOCAL_HOST}:{SSH_CLIENT_LOCAL_PORT}'
    )

    return None
