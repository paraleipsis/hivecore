import asyncio


class PubSub:
    """Object for interacting with channels."""

    def __init__(self):
        self._queues = {}

    def create_channel(self, channel: str) -> None:
        """Create a channel that represents the :class:`Queue` object
           and add it to the dictionary.

           :param channel:
              The channel to create.

        """

        self._queues[channel] = asyncio.Queue()

        return None

    def remove_channel(self, channel: str) -> None:
        """Remove a channel from a :class:`PubSub` object '_queues' dictionary.

           :param channel:
              The channel to remove.

        """

        del self._queues[channel]

        return None


pb = PubSub()
