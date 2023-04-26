from typing import Any

from modules.pubsub.pubsub import PubSub


class Subscriber:
    """Object for interacting with specific channel as a consumer.

       :param pubsub:
          The :class:`PubSub` object which contains all created channels.
       :param channel:
          The channel for receiving messages.

    """

    def __init__(self, pubsub: 'PubSub', channel: str):
        self._channel = pubsub._queues[channel]

    async def get(self) -> Any:
        """Get a message from a channel."""

        message = await self._channel.get()
        self._channel.task_done()

        return message
