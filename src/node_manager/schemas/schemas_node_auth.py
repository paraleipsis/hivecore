from uuid import UUID

from pydantic import BaseModel


class NodeCredentials(BaseModel):
    id: UUID
    token: str


class TokenData(BaseModel):
    node_name: str
    server_pub_key: str
