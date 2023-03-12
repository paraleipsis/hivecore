from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from database import metadata, Base


class Platform(Base):
    __tablename__ = "platform"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True)
    type = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    environments = relationship("Environment", back_populates="platform")


class Environment(Base):
    __tablename__ = "environment"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    platform_id = Column(Integer, ForeignKey("platform.id"))
    platform = relationship("Platform", back_populates="environments")

    nodes = relationship("Node", back_populates="environment")


class Node(Base):
    __tablename__ = "node"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    node_ip = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    environment_id = Column(Integer, ForeignKey("environment.id"))
    environment = relationship("Environment", back_populates="nodes")


# node = Table(
#     "node",
#     metadata,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("name", String, index=True, unique=True),
#     Column("node_ip", String, index=True, unique=True),
#     Column("description", String, index=True),
#     Column("created_at", TIMESTAMP, index=True, default=datetime.utcnow),
#     Column("environment_id", Integer, ForeignKey(environment.c.id)),
# )