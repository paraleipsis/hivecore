from typing import List

from modules.pubsub.pubsub import pb
from logger.logs import logger


def create_pubsub_channels(channels: List[str]) -> None:
    """Creates all provided :class:`PubSub` channels.

    :param channels:
       The channels to create.

    """

    for channel in channels:
        pb.create_channel(channel)

        logger['info'].info(
            f"Created PubSub channel: '{channel}'"
        )

    return None
