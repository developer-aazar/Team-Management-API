from sqlalchemy import Column , Integer , String , DateTime
from sqlalchemy.orm import relationship
from datetime import datetime 
from app.core.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255) , unique=True , index=True , nullable=False)
    hashed_password = Column(String , nullable=False)
    created_at = Column(DateTime , default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime , default=datetime.utcnow , onupdate=datetime.utcnow , nullable=False)
    memberships = relationship("TeamMembership", back_populates="user")

