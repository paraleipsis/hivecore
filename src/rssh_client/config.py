import trafaret as t

from config.utils import load_config
from config.config import BASE_DIR


CONFIG_TRAFARET = t.Dict(
    {
        'SSH_CLIENT_LOCAL_HOST': t.String,
        'SSH_CLIENT_LOCAL_PORT': t.Int,
        'SSH_CLIENT_CLIENT_KEYS': t.String,
        'SSH_CLIENT_KNOWN_HOSTS': t.String,
        'SSH_CLIENT_REUSE_PORT': t.Bool,
        'SSH_CLIENT_MAX_PACKET_SIZE': t.Int,
    }
)


CONF = load_config(
    file=BASE_DIR / 'configs' / 'rssh_client_config.yml',
    config_trafaret=CONFIG_TRAFARET
)


SSH_CLIENT_LOCAL_HOST = CONF['SSH_CLIENT_LOCAL_HOST']
SSH_CLIENT_LOCAL_PORT = CONF['SSH_CLIENT_LOCAL_PORT']
SSH_CLIENT_CLIENT_KEYS = CONF['SSH_CLIENT_CLIENT_KEYS']
SSH_CLIENT_KNOWN_HOSTS = CONF['SSH_CLIENT_KNOWN_HOSTS']
SSH_CLIENT_REUSE_PORT = CONF['SSH_CLIENT_REUSE_PORT']
SSH_CLIENT_MAX_PACKET_SIZE = CONF['SSH_CLIENT_MAX_PACKET_SIZE']
