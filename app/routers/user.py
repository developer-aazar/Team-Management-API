from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.users import UserResponse
from app.models.users import User

router = APIRouter()

@router.get("/users/me" , response_model=UserResponse)
def get_my_info(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)

