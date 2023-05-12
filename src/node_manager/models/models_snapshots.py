import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db.database.database import metadata, Base


class Snapshot(Base):
    __tablename__ = "snapshots"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    snapshot = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    platform_name = Column(String, ForeignKey("platforms.name", ondelete='CASCADE'), nullable=False)
    node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id", ondelete='CASCADE'), nullable=False)
