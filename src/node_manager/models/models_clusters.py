import uuid

from sqlalchemy import TIMESTAMP, Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from sqlalchemy.orm import relationship

from db.database.database import metadata, Base

from node_manager.models.models_nodes import cluster_nodes


# class Environment(Base):
#     __tablename__ = "environments"
#     metadata = metadata
#
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#     name = Column(String, index=True)
#     description = Column(String, index=True)
#     created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)
#
#     platform_id = Column(UUID(as_uuid=True), ForeignKey("platforms.id", ondelete='CASCADE'), nullable=False)
#
#     _table_args__ = (UniqueConstraint(platform_id, name),)


class Cluster(Base):
    __tablename__ = "clusters"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    platform_name = Column(String, ForeignKey("platforms.name", ondelete='CASCADE'), nullable=False)
    nodes = relationship('Node', secondary=cluster_nodes, back_populates="clusters")

