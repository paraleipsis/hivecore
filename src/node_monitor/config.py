import trafaret as t

from config.utils import load_config
from config.config import BASE_DIR
from core.config import AGENT_HOST, AGENT_PORT


CONFIG_TRAFARET = t.Dict(
    {
        'DOCKER_MONITOR': t.Bool,
        'DOCKER_SNAPSHOT_URL': t.String,
        'DOCKER_KAFKA_TOPIC': t.String,
        'DOCKER_KAFKA_PARTITIONS': t.Int,
    }
)


CONF = load_config(
    file=BASE_DIR / 'configs' / 'receiver_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


DOCKER_MONITOR = CONF['DOCKER_MONITOR']
DOCKER_SNAPSHOT_URL = CONF['DOCKER_SNAPSHOT_URL']
DOCKER_KAFKA_TOPIC = CONF['DOCKER_KAFKA_TOPIC']
DOCKER_KAFKA_PARTITIONS = CONF['DOCKER_KAFKA_PARTITIONS']


HOST_MONITOR = {
    'docker': {
        'active': DOCKER_MONITOR,
        'url': f'http://{AGENT_HOST}:{AGENT_PORT}/{DOCKER_SNAPSHOT_URL}',
        'kafka_topic': DOCKER_KAFKA_TOPIC,
        'kafka_partitions': DOCKER_KAFKA_PARTITIONS
    }
}
