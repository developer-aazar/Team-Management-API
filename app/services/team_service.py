from app.core.roles import Role
from fastapi import HTTPException , status
from app.schemas.team import TeamCreate , AddMemberRequest
from app.models.teams import Team
from app.models.team_membership import TeamMembership
from app.models.users import User
from sqlalchemy.orm import Session
from app.core.roles import ROLE_LEVELS


def create_new_team(data: TeamCreate , current_user: User , db: Session) -> Team:

    try:
        new_team = Team(name=data.name , description=data.description)
        db.add(new_team)
        db.flush()

        membership = TeamMembership(team_id=new_team.id , user_id=current_user.id, role="owner")
        db.add(membership)
        db.commit()
        db.refresh(new_team)

        return new_team
    except:
        db.rollback()
        raise 

def  add_new_member(team_id: int , data: AddMemberRequest , db: Session) -> TeamMembership:
    user =  db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    existing_membership = db.query(TeamMembership).filter(TeamMembership.team_id == team_id , TeamMembership.user_id == data.user_id).first()
    if existing_membership:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="user is already a member of this team")

    new_membership = TeamMembership(team_id=team_id , user_id=data.user_id, role="member")

    try:
        db.add(new_membership)
        db.commit()
        db.refresh(new_membership)
        return new_membership
    except Exception:
        db.rollback()
        raise

def remove_member(team_id: int , user_id: int , db: Session , requester_membership: TeamMembership) -> None:
    
    target_membership = db.query(TeamMembership).filter(TeamMembership.team_id==team_id, TeamMembership.user_id==user_id).first()

    if not target_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not member of this team")

    requester_role = ROLE_LEVELS[requester_membership.role]
    target_membership = ROLE_LEVELS[target_membership.role]

    if requester_role <= target_membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot remove a member with an equal or higher role.")

    try: 
        db.delete(target_membership)
        db.commit()

    except Exception:
        db.rollback()
        raise

def promote_member(team_id: int , user_id: int , db: Session, requester_membership: TeamMembership) -> TeamMembership:

    target_membership = db.query(TeamMembership).filter(TeamMembership.team_id==team_id, TeamMembership.user_id==user_id).first()
    
    if not target_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not member of this team.")
    
    if target_membership.role in (Role.ADMIN, Role.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is already an owner or admin.")

    target_membership.role = Role.ADMIN

    try:
        db.add(target_membership)
        db.commit()
        db.refresh(target_membership)

        return target_membership

    except Exception:
        db.rollback()
        raise

def demote_member(team_id: int , user_id: int , db: Session, requester_membership: TeamMembership) -> TeamMembership:
    target_membership = db.query(TeamMembership).filter(TeamMembership.team_id == team_id , TeamMembership.user_id == user_id).first()

    if not target_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not member of this team.")
    
    if target_membership.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't demote an owner or a member.")

    target_membership.role = Role.MEMBER

    try:
        db.commit()
        db.refresh(target_membership)
        return target_membership

    except Exception:
        db.rollback()
        raise
            
def leave_team(team_id: int ,  db: Session, requester_membership: TeamMembership) -> None:
    try:
        db.delete(requester_membership)
        db.commit()
        
    except Exception:
        db.rollback()
        raise



