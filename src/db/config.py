import trafaret as t

from config.utils import load_config
from config.agent_config import BASE_DIR


CONFIG_TRAFARET = t.Dict(
    {
        'KAFKA_HOST': t.String,
        'KAFKA_PORT': t.Int,
        'DB_USER': t.String,
        'DB_PASS': t.String,
        'DB_HOST': t.String,
        'DB_PORT': t.String,
        'DB_NAME': t.String,
        'DOCKER_KAFKA_TOPIC': t.String,
        'DOCKER_KAFKA_PARTITIONS': t.Int,
    }
)


CONF = load_config(
    file=BASE_DIR / 'configs' / 'storage_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


KAFKA_HOST = CONF['KAFKA_HOST']
KAFKA_PORT = CONF['KAFKA_PORT']

DB_USER = CONF['DB_USER']
DB_PASS = CONF['DB_PASS']
DB_HOST = CONF['DB_HOST']
DB_PORT = CONF['DB_PORT']
DB_NAME = CONF['DB_NAME']

DOCKER_KAFKA_TOPIC = CONF['DOCKER_KAFKA_TOPIC']
DOCKER_KAFKA_PARTITIONS = CONF['DOCKER_KAFKA_PARTITIONS']
