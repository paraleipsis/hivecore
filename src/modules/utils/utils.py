import hashlib
import json
from typing import Any


def get_hash_of_obj(obj: Any) -> str:
    return hashlib.md5(json.dumps(obj).encode("utf-8")).hexdigest()


def is_equal(old_object: Any, new_object: Any) -> bool:
    old_hash = get_hash_of_obj(old_object)
    new_hash = get_hash_of_obj(new_object)

    return old_hash == new_hash
