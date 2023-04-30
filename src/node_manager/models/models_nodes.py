import uuid

from sqlalchemy import TIMESTAMP, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db.database.database import metadata, Base


class Node(Base):
    __tablename__ = "nodes"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    node_ip = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    environment_id = Column(UUID(as_uuid=True), ForeignKey("environments.id", ondelete='CASCADE'), nullable=False)

    _table_args__ = (UniqueConstraint(environment_id, name),)
