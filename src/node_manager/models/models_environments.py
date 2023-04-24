import uuid

from sqlalchemy import TIMESTAMP, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db.database import metadata, Base


class Environment(Base):
    __tablename__ = "environments"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    platform_id = Column(UUID(as_uuid=True), ForeignKey("platforms.id", ondelete='CASCADE'), nullable=False)

    _table_args__ = (UniqueConstraint(platform_id, name),)
