import asyncio
from asyncio import AbstractEventLoop
from typing import Optional, Dict

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from db.broker.utils import key_serializer, value_serializer, key_deserializer, value_deserializer
from db.config import KAFKA_HOST, KAFKA_PORT
from logger.logs import logger

KAFKA_URL = f"{KAFKA_HOST}:{KAFKA_PORT}"

# _kafka_loop = asyncio.get_running_loop()

_kafka_producer: Optional[AIOKafkaProducer] = None


def get_kafka_loop() -> AbstractEventLoop:
    loop = asyncio.get_running_loop()
    return loop


def get_kafka_producer() -> Optional[AIOKafkaProducer]:
    return _kafka_producer


async def run_kafka_producer() -> Optional[AIOKafkaProducer]:
    global _kafka_producer

    try:
        _kafka_producer = AIOKafkaProducer(
            loop=get_kafka_loop(),
            bootstrap_servers=KAFKA_URL,
            key_serializer=key_serializer,
            value_serializer=value_serializer,
            compression_type="gzip",
        )

        await _kafka_producer.start()
    except Exception as exc:
        logger['error'].error(
            f"Error starting Kafka Producer:\n{repr(exc)}"
        )

    return _kafka_producer


async def produce(
        topic: str,
        key: str,
        value: Dict,
) -> None:
    try:
        await _kafka_producer.send_and_wait(topic=topic, key=key, value=value)
        logger['error'].error(
            f"Kafka Message sent to topic '{topic}'"
        )
    except Exception as exc:
        logger['error'].error(
            f"Exception in sending JSON message to Kafka Topic '{topic}':\n{repr(exc)}"
        )

    return None


# TODO: add yield type hint
async def consume(topic: str, **kwargs):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_URL,
        loop=get_kafka_loop(),
        key_deserializer=key_deserializer,
        value_deserializer=value_deserializer,
        **kwargs
    )

    await consumer.start()

    try:
        async for msg in consumer:
            yield msg
    except Exception as exc:
        logger['error'].error(
            f"Consumer Error in Kafka Topic '{topic}':\n{repr(exc)}"
        )
    finally:
        await consumer.stop()
