import trafaret as t

from config.utils import load_config
from config.agent_config import BASE_DIR


from config.agent_config import AGENT_URL

CONFIG_TRAFARET = t.Dict(
    {
        'ACTIVE_PLATFORMS_RSSH_ROUTER': t.String,
        'SNAPSHOT_RSSH_ROUTER': t.String,
        'DOCKER_SNAPSHOT_URL': t.String,
        'SWARM_SNAPSHOT_URL': t.String,
        'ACTIVE_PLATFORMS_URL': t.String,
        'NODES_URL': t.String,
        'NODE_STATUS_URL': t.String,
        'NODE_PLATFORM_URL': t.String,
        'NODE_SNAPSHOT_URL': t.String,
    }
)


CONF = load_config(
    file=BASE_DIR / 'node_monitor_config.yml',
    config_trafaret=CONFIG_TRAFARET
)

NODES_URL = CONF['NODES_URL']
NODE_STATUS_URL = CONF['NODE_STATUS_URL']
NODE_PLATFORM_URL = CONF['NODE_PLATFORM_URL']
NODE_SNAPSHOT_URL = CONF['NODE_SNAPSHOT_URL']

ACTIVE_PLATFORMS_RSSH_ROUTER = CONF['ACTIVE_PLATFORMS_RSSH_ROUTER']
ACTIVE_PLATFORMS_URL = f"{AGENT_URL}/{CONF['ACTIVE_PLATFORMS_URL']}"

SNAPSHOT_RSSH_ROUTER = CONF['SNAPSHOT_RSSH_ROUTER']
DOCKER_SNAPSHOT_URL = f"{AGENT_URL}/{CONF['DOCKER_SNAPSHOT_URL']}"
