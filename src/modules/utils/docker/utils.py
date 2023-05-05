from typing import Any

from modules.exc.exceptions.exceptions_docker import NoSuchDockerObject


def get_docker_object_by_id(object_id: str, docker_object: Any) -> Any:
    result_list = list(
        map(
            lambda x: x,
            filter(
                lambda x: x.Id.startswith(object_id), docker_object
            )
        )
    )

    if not result_list:
        raise NoSuchDockerObject('Docker object with such ID not found')

    result = result_list[0]

    return result
