import trafaret as t

from config.utils import load_config
from config.agent_config import CONFIGS_BASE_DIR
from modules.utils.utils import read_file

SSH_CONFIG_FILE = 'ssh_keys_config.yml'


SSH_CONFIG_TRAFARET = t.Dict(
    {
        'SSH_PRIVATE_KEY_PATH': t.String,
        'SSH_PUBLIC_KEY_PATH': t.String,
    }
)


SSH_CONF = load_config(
    file=CONFIGS_BASE_DIR / SSH_CONFIG_FILE,
    config_trafaret=SSH_CONFIG_TRAFARET
)

SSH_PUBLIC_KEY_PATH = CONFIGS_BASE_DIR.parent / SSH_CONF['SSH_PUBLIC_KEY_PATH']
SSH_PUBLIC_KEY = read_file(path=SSH_PUBLIC_KEY_PATH)
