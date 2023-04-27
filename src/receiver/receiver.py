# in cycle:

# 1. listen to PubSub Channel anf receive object of UUID and SSH Channel to connect;

# 2. establish STREAM connection to WS router on Reverse SSH Server that in turn
# should establish a WebSocket connection to hivecore-agent aiohttp server to report
# application by some endpoint;

# 3. receive data;

# 4. Kafka Stream - Faust: send received data to appropriate topics.


import asyncio

from modules.pubsub.pubsub import pb
from modules.pubsub.subscriber import Subscriber
from rssh_client.rssh import rssh_client
from logger.logs import logger


sub = Subscriber(pubsub=pb, channel='connections')


async def receiver() -> None:
    while True:
        msg = await sub.get()
        print(msg)


def run_receiver() -> None:
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(coro=receiver(), loop=loop)

    logger['info'].info(
        f'Receiver is running'
    )

    return None
