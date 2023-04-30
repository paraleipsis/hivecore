import trafaret as t

from config.utils import load_config
from config.config import BASE_DIR


CONFIG_TRAFARET = t.Dict(
    {
        'KAFKA_HOST': t.String,
        'KAFKA_PORT': t.Int,
        'KAFKA_FAUST_APP_ID': t.String,
        'DB_USER': t.String,
        'DB_PASS': t.String,
        'DB_HOST': t.String,
        'DB_PORT': t.Int,
        'DB_NAME': t.String,
    }
)


CONF = load_config(
    file=BASE_DIR / 'configs' / 'storage_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


KAFKA_HOST = CONF['KAFKA_HOST']
KAFKA_PORT = CONF['KAFKA_PORT']
KAFKA_FAUST_APP_ID = CONF['KAFKA_FAUST_APP_ID']

DB_USER = CONF['DB_USER']
DB_PASS = CONF['DB_PASS']
DB_HOST = CONF['DB_HOST']
DB_PORT = CONF['DB_PORT']
DB_NAME = CONF['DB_NAME']
