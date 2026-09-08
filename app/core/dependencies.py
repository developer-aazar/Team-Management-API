from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from jose import JWTError
from app.models.users import User
from app.core.security import verify_access_token
from app.models.team_membership import TeamMembership


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Token",
    headers={"WWW-Authenticate": "Bearer"})

bearer_scheme = HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    try:
        payload = verify_access_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        user_id = int(sub)  
    except (JWTError , ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user

def get_team_membership(team_id: int , current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> TeamMembership:
    membership = db.query(TeamMembership).filter(
        TeamMembership.team_id == team_id,
        TeamMembership.user_id == current_user.id   
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this team."
        )
    return membership

    
def required_roles(*allowed_roles):
    def check_role(membership: TeamMembership = Depends(get_team_membership)):
        print("MEMBERSHIP ROLE:", membership.role)
        print("ALLOWED ROLES:", allowed_roles)
        if membership.role not in allowed_roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN , detail="Insufficient Permissions")
        return membership

    return check_role
