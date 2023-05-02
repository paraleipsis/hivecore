import asyncio

from rssh_client.rssh import get_rssh_client
from rssh_client.config import SSH_CLIENT_LOCAL_HOST, SSH_CLIENT_LOCAL_PORT
from logger.logs import logger


def run_rssh_client() -> None:
    """Run the Reverse SSH Client Listener in a separate thread."""

    loop = asyncio.get_event_loop()
    rssh_client = get_rssh_client()
    loop.run_in_executor(None, rssh_client.start)

    logger['info'].info(
        f'Reverse SSH Client running on {SSH_CLIENT_LOCAL_HOST}:{SSH_CLIENT_LOCAL_PORT}'
    )

    return None
