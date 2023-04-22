import logging.config
import yaml

from pathlib import Path


def load_config():
    with open(Path(__file__).resolve().parent / 'config.yml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    configs = {
        'error': logging.getLogger('errorLogger'),
        'info': logging.getLogger('infoLogger'),
        'debug': logging.getLogger('debugLogger'),
    }

    return configs


logger = load_config()
