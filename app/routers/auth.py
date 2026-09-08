from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.core.security import hash_password, verify_password , create_access_token
from app.core.database import get_db
from app.models.users import User
from app.schemas.auth import SignupRequest , SignupResponse , LoginRequest , LoginResponse

router = APIRouter(prefix= "/auth")

@router.post("/signup", response_model=SignupResponse , status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest , db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail="User Already Exists")
    
    new_user = User(full_name= data.full_name,email = data.email , hashed_password = hash_password(data.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return SignupResponse(
        id = new_user.id,
        full_name = new_user.full_name,
        email = new_user.email)

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password , user.hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": str(user.id)})

    return LoginResponse(access_token = access_token, token_type = "bearer")

