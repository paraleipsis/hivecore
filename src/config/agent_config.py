import pathlib

import trafaret as t

from config.utils import load_config


BASE_DIR = pathlib.Path(__file__).parent

CONFIG_TRAFARET = t.Dict(
    {
        'AGENT_HOST': t.String,
        'AGENT_PORT': t.Int,
        'DOCKER_START_CONTAINER': t.String,
    }
)


CONF = load_config(
    file=BASE_DIR / 'configs' / 'agent_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


AGENT_HOST = CONF['AGENT_HOST']
AGENT_PORT = CONF['AGENT_PORT']

AGENT_URL = f'http://{AGENT_HOST}:{AGENT_PORT}'

DOCKER_START_CONTAINER = CONF['DOCKER_START_CONTAINER']
