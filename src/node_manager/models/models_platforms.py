import uuid

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from sqlalchemy.orm import relationship

from db.database.database import metadata, Base

from node_manager.models.models_nodes import platform_nodes


class Platform(Base):
    __tablename__ = "platforms"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True)
    type = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    nodes = relationship('Node', secondary=platform_nodes, back_populates="platforms")
