import asyncio

from rssh_client.rssh import rssh_client
from rssh_client.config import SSH_CLIENT_LOCAL_HOST, SSH_CLIENT_LOCAL_PORT
from logger.logs import logger


def run_rssh_client():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, rssh_client.start)

    logger['info'].info(
        f'Reverse SSH Client running on http://{SSH_CLIENT_LOCAL_HOST}:{SSH_CLIENT_LOCAL_PORT}'
    )
