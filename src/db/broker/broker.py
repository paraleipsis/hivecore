import asyncio

import faust

from db.config import KAFKA_HOST, KAFKA_PORT, KAFKA_FAUST_APP_ID

KAFKA_URL = f"kafka://{KAFKA_HOST}:{KAFKA_PORT}"

kafka_event_loop = asyncio.get_event_loop()

faust_app = faust.App(
    id=KAFKA_FAUST_APP_ID,
    broker=KAFKA_URL,
    value_serializer='raw',
    loop=kafka_event_loop
)
