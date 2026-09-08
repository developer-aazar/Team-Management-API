from pydantic import BaseModel , EmailStr , ConfigDict
from datetime import datetime


class UserResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int 
    full_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime