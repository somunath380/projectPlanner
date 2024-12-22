from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import List, Optional, Text

def get_utc_now():
    return datetime.now(timezone.utc)

class UsersOfTeam(BaseModel):
    id: int
    name: str

class ProjectsOfTeam(BaseModel):
    id: int
    name: Text = Field(..., min_length=4, frozen=True, max_length=64)

class TeamBase(BaseModel):
    id: int
    name: str = Field(..., min_length=4, frozen=True, max_length=64)
    description: str = Field(..., min_length=4, frozen=True, max_length=128)
    admin: int = Field(..., frozen=True)
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)
    users: Optional[List[UsersOfTeam]] = []
    projects: Optional[List[ProjectsOfTeam]] = []

class TeamCreateRequestSchema(BaseModel):
    name: str = Field(min_length=4, frozen=True, max_length=64)
    description: str = Field(..., min_length=4, frozen=True, max_length=128)
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)
    admin: int = Field(..., frozen=True)

class TeamCreateResponseSchema(BaseModel):
    id: int

class GetTeamDetailsRequestSchema(BaseModel):
    id: int

class GetTeamDetailsResponseSchema(BaseModel):
    name: str
    description: str
    created_at: datetime
    admin: int

class TeamUpdateDataSchema(BaseModel):
    name: str = Field(..., frozen=True, max_length=64)
    description: str = Field(..., frozen=True, max_length=128)
    admin: int

class TeamUpdateRequestSchema(BaseModel):
    id: int = Field(..., example="<team_id>")
    team: TeamUpdateDataSchema

class AddRemoveUsersToTeamsRequestSchema(BaseModel):
    id: int = Field(..., description="The unique identifier for the team")
    users: List[int] = Field(
        ..., 
        description="List of user IDs to be added to the team", 
        max_items=50  # Enforces the max number of items in the list
    )



