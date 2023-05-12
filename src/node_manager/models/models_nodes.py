import uuid

from sqlalchemy import TIMESTAMP, Column, String, ForeignKey, UniqueConstraint, JSON, BOOLEAN, Integer, Table
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from sqlalchemy.orm import relationship

from db.database.database import metadata, Base

# class Node(Base):
#     __tablename__ = "nodes"
#     metadata = metadata
#
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#     active = Column(BOOLEAN, nullable=False)
#     name = Column(String, index=True)
#     description = Column(String, index=True)
#     created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)
#     docker_snapshot = Column(JSON, nullable=True)
#     swarm_snapshot = Column(JSON, nullable=True)
#
#     environment_id = Column(UUID(as_uuid=True), ForeignKey("environments.id", ondelete='CASCADE'), nullable=False)
#
#     _table_args__ = (UniqueConstraint(environment_id, name),)


platform_nodes = Table("platform_nodes", metadata,
                       Column("id", UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4),
                       Column("platform_name", ForeignKey("platforms.name"), primary_key=True),
                       Column("node_id", ForeignKey("nodes.id"), primary_key=True))

cluster_nodes = Table("cluster_nodes", metadata,
                      Column("id", UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4),
                      Column("cluster_id", ForeignKey("clusters.id"), primary_key=True),
                      Column("node_id", ForeignKey("nodes.id"), primary_key=True))


class Node(Base):
    __tablename__ = "nodes"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    active = Column(BOOLEAN, default=False)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)
    server_ipv4 = Column(String, index=True, nullable=False)

    platforms = relationship('Platform', secondary=platform_nodes, back_populates="nodes")
    clusters = relationship('Cluster', secondary=cluster_nodes, back_populates="nodes")
    snapshots = relationship('Snapshot', backref="nodes")
