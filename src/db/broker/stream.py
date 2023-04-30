import json

from typing import Dict

import faust

from logger.logs import logger


class TopicStreamHandler:
    def __init__(
            self,
            topic: str,
            topic_partitions: int,
            faust_stream_app: faust.App,
            encoding: str = 'utf-8',
    ):
        self.faust_stream_app = faust_stream_app

        self.topic = self.faust_stream_app.topic(
            topic,
            partitions=topic_partitions,
        )
        self.encoding = encoding

    async def send_json_message(self, key: str, value: Dict) -> None:
        try:
            await self.topic.send(
                key=key.encode(self.encoding),
                value=json.dumps(value).encode(self.encoding)
            )
        except Exception as exc:
            logger['debug'].debug(
                f"Exception in sending JSON message to Kafka Topic '{self.topic}':\n{repr(exc)}"
            )

        return None

    async def send_message(self, key: str, value: str) -> None:
        try:
            await self.topic.send(
                key=key.encode(self.encoding),
                value=value.encode(self.encoding)
            )
        except Exception as exc:
            logger['debug'].debug(
                f"Exception in sending message to Kafka Topic '{self.topic}':\n{str(exc)}"
            )

        return None
