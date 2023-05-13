from typing import Any

import yaml


def get_yaml_data(file: str) -> Any:
    with open(file, 'r') as file:
        data = yaml.safe_load(file)

    return data


def write_yaml_data(file: str, data: Any) -> None:
    with open(file, 'w') as file:
        yaml.safe_dump(data, file, default_flow_style=False)

    return None
