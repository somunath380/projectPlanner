from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Optional

def get_utc_now():
    return datetime.now(timezone.utc)

class TeamsOfUser(BaseModel):
    id: int
    name: str

class UserBase(BaseModel):
    id: int
    name: str = Field(min_length=4, frozen=True, max_length=64)
    display_name: str = Field(min_length=4, frozen=True, max_length=64)
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)
    teams: Optional[List[TeamsOfUser]] = [] 

class UserCreateRequestSchema(BaseModel):
    name: str = Field(min_length=4, frozen=True, max_length=64)
    display_name: str = Field(min_length=4, frozen=True, max_length=64)
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)

class UserCreateResponseSchema(UserBase):
    id: int

class UserGetAll(BaseModel):
    name: str
    display_name: str
    created_at: datetime

class UserGetResponse(UserGetAll):
    pass

class UpdatedUser(BaseModel):
    name: str = Field(..., frozen=True, max_length=64)
    display_name: str = Field(..., frozen=True, max_length=128)

class UpdateUserSchema(BaseModel):
    id: int = Field(..., example="<user_id>")
    user: UpdatedUser
