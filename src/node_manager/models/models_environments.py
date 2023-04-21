from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey, UniqueConstraint
from datetime import datetime

from sqlalchemy.orm import relationship

from database import metadata, Base


class Environment(Base):
    __tablename__ = "environments"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete='CASCADE'), nullable=False)
    platform = relationship("Platform", back_populates="environments")

    nodes = relationship("Node", back_populates="environment", passive_deletes='all')

    _table_args__ = (UniqueConstraint(platform_id, name),)
