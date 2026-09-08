from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    full_name: str = Field(min_length=3 , max_length=100 , strip_whitespace=True)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

class SignupResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100 , strip_whitespace=True)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    