import trafaret as t

from config.utils import load_config
from config.config import CONFIGS_BASE_DIR

CONFIG_FILE = 'storage_config.yml'


CONFIG_TRAFARET = t.Dict(
    {
        'KAFKA_HOST': t.String,
        'KAFKA_PORT': t.Int,
        'DB_USER': t.String,
        'DB_PASS': t.String,
        'DB_HOST': t.String,
        'DB_PORT': t.String,
        'DB_NAME': t.String,
        'DOCKER_PLATFORM_NAME': t.String,
        'DOCKER_TYPE': t.String,
        'DOCKER_DESCRIPTION': t.String,
        'SWARM_PLATFORM_NAME': t.String,
        'SWARM_TYPE': t.String,
        'SWARM_DESCRIPTION': t.String,
    }
)


CONF = load_config(
    file=CONFIGS_BASE_DIR / CONFIG_FILE,
    config_trafaret=CONFIG_TRAFARET
)


KAFKA_HOST = CONF['KAFKA_HOST']
KAFKA_PORT = CONF['KAFKA_PORT']

DB_USER = CONF['DB_USER']
DB_PASS = CONF['DB_PASS']
DB_HOST = CONF['DB_HOST']
DB_PORT = CONF['DB_PORT']
DB_NAME = CONF['DB_NAME']

DOCKER_PLATFORM_NAME = CONF['DOCKER_PLATFORM_NAME']
DOCKER_TYPE = CONF['DOCKER_TYPE']
DOCKER_DESCRIPTION = CONF['DOCKER_DESCRIPTION']
SWARM_PLATFORM_NAME = CONF['SWARM_PLATFORM_NAME']
SWARM_TYPE = CONF['SWARM_TYPE']
SWARM_DESCRIPTION = CONF['SWARM_DESCRIPTION']
