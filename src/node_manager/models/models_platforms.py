from sqlalchemy import TIMESTAMP, Column, Integer, String
from datetime import datetime

from sqlalchemy.orm import relationship

from database import metadata, Base


class Platform(Base):
    __tablename__ = "platforms"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True)
    type = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True, default=datetime.utcnow)

    environments = relationship("Environment", back_populates="platform", passive_deletes='all')
