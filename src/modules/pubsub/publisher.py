from typing import Any

from modules.pubsub.pubsub import PubSub


class Publisher:
    """Object for sending messages to channels as a producer.

       :param pubsub:
          The :class:`PubSub` object which contains all created channels.

    """

    def __init__(self, pubsub: 'PubSub'):
        self._channels = pubsub._queues

    async def publish(self, channel: str, message: Any) -> None:
        """Send a message to a specific channel.

           :param channel:
              The channel to send.
           :param message:
              The object to send.

        """

        await self._channels[channel].put(message)

        return None

    async def broadcast(self, message: Any) -> None:
        """Send a message to all created channels.

           :param message:
              The object to send.

        """

        for queue in self._channels:
            await queue.put(message)

        return None
