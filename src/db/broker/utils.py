import json


def value_serializer(value: str, encoding: str = 'utf-8'):
    return json.dumps(value).encode(encoding=encoding)


def key_serializer(key: str, encoding: str = 'utf-8'):
    return key.encode(encoding=encoding)


def value_deserializer(value: bytes):
    return json.loads(value)


def key_deserializer(key: bytes, encoding: str = 'utf-8'):
    return key.decode(encoding=encoding)
