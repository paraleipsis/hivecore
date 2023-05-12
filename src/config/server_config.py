import trafaret as t

from config.config import BASE_DIR
from config.utils import load_config


CONFIG_TRAFARET = t.Dict(
    {
        'HOST': t.String,
        'PORT': t.Int,
        'LOG_LEVEL': t.String,
        'DOCS_URL': t.String,
        'OPENAPI_URL': t.String,
        'PUBSUB_CHANNELS': t.List(t.String),
    }
)


CONF = load_config(
    file=BASE_DIR / 'core_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


HOST = CONF['HOST']
PORT = CONF['PORT']
SERVER_URL = f'http://{HOST}:{PORT}'
LOG_LEVEL = CONF['LOG_LEVEL']
DOCS_URL = CONF['DOCS_URL']
OPENAPI_URL = CONF['OPENAPI_URL']

PUBSUB_CHANNELS = CONF['PUBSUB_CHANNELS']
