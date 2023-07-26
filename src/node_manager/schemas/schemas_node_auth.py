from uuid import UUID

from pydantic import BaseModel


class NodeCredentials(BaseModel):
    node_id: UUID
    token: str


class TokenData(BaseModel):
    node_name: str
    server_pub_key: str
    server_ipv4: str
