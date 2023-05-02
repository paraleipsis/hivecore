import trafaret as t

from config.utils import load_config
from config.agent_config import BASE_DIR
from config.agent_config import AGENT_HOST, AGENT_PORT, AGENT_URL
from db.config import DOCKER_KAFKA_TOPIC, DOCKER_KAFKA_PARTITIONS


CONFIG_TRAFARET = t.Dict(
    {
        'DOCKER_MONITOR': t.Bool,
        'DOCKER_SNAPSHOT_URL': t.String,
    }
)


CONF = load_config(
    file=BASE_DIR / 'configs' / 'node_monitor_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


DOCKER_MONITOR = CONF['DOCKER_MONITOR']
DOCKER_SNAPSHOT_URL = CONF['DOCKER_SNAPSHOT_URL']


HOST_MONITOR = {
    'docker': {
        'active': DOCKER_MONITOR,
        'url': f'{AGENT_URL}/{DOCKER_SNAPSHOT_URL}',
        'kafka_topic': DOCKER_KAFKA_TOPIC,
        'kafka_partitions': DOCKER_KAFKA_PARTITIONS
    }
}
