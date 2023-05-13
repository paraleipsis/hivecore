import trafaret as t

from config.config import CONFIGS_BASE_DIR
from config.utils import load_config

CONFIG_FILE = 'auth_config.yml'


CONFIG_TRAFARET = t.Dict(
    {
        'SECRET_KEY': t.String,
        'ALGORITHM': t.String,
        'ACCESS_TOKEN_EXPIRE_MINUTES': t.Int
    }
)


CONF = load_config(
    file=CONFIGS_BASE_DIR / CONFIG_FILE,
    config_trafaret=CONFIG_TRAFARET
)

SECRET_KEY = CONF['SECRET_KEY']
ALGORITHM = CONF['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = CONF['ACCESS_TOKEN_EXPIRE_MINUTES']
