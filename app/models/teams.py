from app.core.database import Base
from sqlalchemy import Column, Integer , String , DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer , primary_key=True)
    name = Column(String(100) , nullable=False)
    description = Column(String(255) , nullable=True)
    created_at = Column(DateTime , default=datetime.utcnow , nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow , onupdate=datetime.utcnow , nullable=False)
    memberships = relationship("TeamMembership", back_populates="team" , cascade="all, delete-orphan")
