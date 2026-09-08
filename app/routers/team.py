from app.models.team_membership import TeamMembership
from fastapi import APIRouter, Depends, status , HTTPException
from app.services.team_service import create_new_team , add_new_member, remove_member, promote_member, demote_member, leave_team
from app.core.dependencies import get_current_user , required_roles
from app.core.database import get_db
from app.core.roles import Role
from app.schemas.team import TeamCreate , TeamResponse , AddMemberRequest , AddMemberResponse
from app.models.users import User
from app.models.teams import Team
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()

@router.post("/teams" , response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(data: TeamCreate , current_user = Depends(get_current_user) , db = Depends(get_db)) -> TeamResponse:
    new_team = create_new_team(data , current_user , db)
    return TeamResponse(id=new_team.id , name=new_team.name , description=new_team.description)


@router.post("/teams/{team_id}/members", response_model=AddMemberResponse , status_code=status.HTTP_201_CREATED)
def add_member(team_id: int , data: AddMemberRequest ,  db: Session = Depends(get_db), membership : TeamMembership = Depends(required_roles(Role.ADMIN , Role.OWNER))):
    member = add_new_member(team_id , data , db)
    return member

@router.delete("/teams/{team_id}/members/me", status_code=status.HTTP_204_NO_CONTENT)
def leave_current_team(team_id: int , db: Session = Depends(get_db), requester_membership: TeamMembership = Depends(required_roles(Role.MEMBER, Role.ADMIN))):
    print("LEAVE ROUTE LOADED....")
    leave_team(team_id , db , requester_membership)

@router.delete("/teams/{team_id}/members/{user_id}" , status_code=status.HTTP_204_NO_CONTENT)
def remove_team_member(team_id: int , user_id: int , db: Session = Depends(get_db) , requester_membership: TeamMembership = Depends(required_roles(Role.OWNER , Role.ADMIN))): 
    member = remove_member(team_id , user_id, db, requester_membership)
    
@router.get("/teams/{team_id}", response_model=List[TeamResponse])
def get_team_data(db: Session = Depends(get_db) , required_role: TeamMembership = Depends(required_roles(Role.ADMIN, Role.OWNER))):
    team_data = db.query(Team).all()

    if not team_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team Not Found")

    return team_data


@router.patch("/teams/{team_id}/members/{user_id}/promote", response_model=AddMemberResponse)
def promote_to_admin(team_id: int , user_id: int , db: Session = Depends(get_db), requester_membership : TeamMembership = Depends(required_roles(Role.OWNER))):
    promoted_member = promote_member(team_id , user_id , db, requester_membership)

    return promoted_member
    
@router.patch("/teams/{team_id}/members/{user_id}/demote", response_model=AddMemberResponse)
def demote_from_admin(team_id: int , user_id: int , db: Session = Depends(get_db), requester_membership: TeamMembership = Depends(required_roles(Role.OWNER))):
    demoted_member = demote_member(team_id , user_id , db , requester_membership)

    return demoted_member



