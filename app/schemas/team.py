from pydantic import BaseModel, Field , ConfigDict
from datetime import datetime

class TeamCreate(BaseModel):
    name: str = Field(min_length=5 , max_length=50)
    description: str | None = Field(default=None, min_length=10 , max_length=250)


class TeamResponse(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=5 , max_length=50)
    description: str | None = Field(default=None, min_length=10 , max_length=250)


class AddMemberRequest(BaseModel):
    user_id: int = Field(gt=0)

class AddMemberResponse(BaseModel):
    id : int
    team_id : int
    user_id : int
    role : str 
    joined_at : datetime

    model_config = ConfigDict(from_attributes=True)
    