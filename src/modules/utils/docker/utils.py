from typing import Any


def get_docker_object_by_id(object_id: str, docker_object: Any) -> Any:
    result_list = list(
        map(
            lambda x: x,
            filter(
                lambda x: x.Id.startswith(object_id), docker_object
            )
        )
    )
    result = result_list[0]

    return result
