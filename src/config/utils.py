import trafaret as t
import yaml
from pathlib import Path


def load_config(
        file: str | Path,
        config_trafaret: t.Dict
):
    with open(file, 'rt') as f:
        data = yaml.safe_load(f)

    return config_trafaret.check(data)
