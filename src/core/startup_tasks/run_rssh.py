import asyncio

from rssh_client.rssh import rssh_client


def run_rssh_client():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, rssh_client.start)
