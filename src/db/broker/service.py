from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from db.storage_config import KAFKA_PORT, KAFKA_HOST, DOCKER_PLATFORM_NAME, SWARM_PLATFORM_NAME
from logger.logs import logger


# TODO: fix IncompatibleBrokerVersion("Kafka broker does not support the 'CreateTopicsRequest_v0' Kafka protocol.")
async def init_topics():
    try:
        admin_client = AIOKafkaAdminClient(
            bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
            client_id='init_topics'
        )

        topic_list = [
            NewTopic(name=DOCKER_PLATFORM_NAME, num_partitions=8, replication_factor=1),
            NewTopic(name=SWARM_PLATFORM_NAME, num_partitions=8, replication_factor=1)
        ]
        await admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except Exception as exc:
        logger['error'].error(
            f"Error creating Kafka topics:\n{repr(exc)}"
        )
