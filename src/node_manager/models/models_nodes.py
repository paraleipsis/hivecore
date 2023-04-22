from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey, UniqueConstraint
from datetime import datetime

from sqlalchemy.orm import relationship

from db.database import metadata, Base


class Node(Base):
    __tablename__ = "nodes"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    node_ip = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    environment_id = Column(Integer, ForeignKey("environments.id", ondelete='CASCADE'), nullable=False)
    environment = relationship("Environment", back_populates="nodes")

    _table_args__ = (UniqueConstraint(environment_id, name),)
