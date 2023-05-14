import hashlib
import json
from typing import Any, Mapping


def clean_map(obj: Mapping[Any, Any]) -> Mapping[Any, Any]:
    """
    Return a new copied dictionary without the keys with ``None`` values from
    the given Mapping object.
    """
    return {k: v for k, v in obj.items() if v is not None}


def get_hash_of_obj(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj).encode("utf-8")).hexdigest()


def is_equal(old_object: Any, new_object: Any) -> bool:
    old_hash = get_hash_of_obj(old_object)
    new_hash = get_hash_of_obj(new_object)

    return old_hash == new_hash


def read_file(path: str) -> Any:
    with open(file=path, mode='r') as f:
        data = f.read()

    return data
