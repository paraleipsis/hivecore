from redis_om import JsonModel, EmbeddedJsonModel
from typing import List
from uuid import UUID
from db.database import redis_connection


class Node(EmbeddedJsonModel):
    id: UUID
    name: str
    ip: str


class Environment(EmbeddedJsonModel):
    name: str
    nodes: List[Node]


class Docker(JsonModel):
    environments: List[Environment]

    class Meta:
        database = redis_connection
