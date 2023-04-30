import trafaret as t

from config.utils import load_config
from config.config import BASE_DIR


CONFIG_TRAFARET = t.Dict(
    {
        'HOST': t.String,
        'PORT': t.Int,
        'LOG_LEVEL': t.String,
        'DOCS_URL': t.String,
        'OPENAPI_URL': t.String,
        'AGENT_HOST': t.String,
        'AGENT_PORT': t.Int,
        'PUBSUB_CHANNELS': t.List(t.String),
        'NODE_MONITOR_RSSH_HOST_ROUTER': t.String,
    }
)


CONF = load_config(
    file=BASE_DIR / 'configs' / 'core_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


AGENT_HOST = CONF['AGENT_HOST']
AGENT_PORT = CONF['AGENT_PORT']

HOST = CONF['HOST']
PORT = CONF['PORT']
LOG_LEVEL = CONF['LOG_LEVEL']
DOCS_URL = CONF['DOCS_URL']
OPENAPI_URL = CONF['OPENAPI_URL']

PUBSUB_CHANNELS = CONF['PUBSUB_CHANNELS']

NODE_MONITOR_RSSH_HOST_ROUTER = CONF['NODE_MONITOR_RSSH_HOST_ROUTER']
