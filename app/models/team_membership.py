from app.core.database import Base
from sqlalchemy import Column, Integer, String , ForeignKey , DateTime , UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.teams import Team
from app.models.users import User

class TeamMembership(Base):
    __tablename__ = "team_memberships"

    __table_args__ = (
        UniqueConstraint('team_id', 'user_id'),
    )

    id = Column(Integer , primary_key=True)
    team_id = Column(Integer , ForeignKey("teams.id") , nullable=False)
    user_id = Column(Integer , ForeignKey("users.id"), nullable=False)
    role = Column(String(50) , default="member" , nullable=False)
    joined_at = Column(DateTime , default=datetime.utcnow , nullable=False)
    team = relationship("Team", back_populates="memberships")
    user = relationship("User", back_populates="memberships")
    