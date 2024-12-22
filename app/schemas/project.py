from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, timezone
from typing import List, Optional, Text
from enum import Enum


def get_utc_now():
    return datetime.now(timezone.utc)

class TaskStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class TasksBase(BaseModel):
    id: int
    name: Text = Field(..., min_length=4, frozen=True, max_length=64)
    description: Text = Field(..., min_length=4, frozen=True, max_length=128)
    user_id: int
    status: TaskStatus = TaskStatus.OPEN
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)

class TaskStatusUpdateRequestSchema(BaseModel):
    id: int
    status: TaskStatus

class TeamsOfProject(BaseModel):
    id: int

class ProjectStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class ProjectBase(BaseModel):
    id: int
    name: Text = Field(..., min_length=4, frozen=True, max_length=64)
    description: str = Field(..., min_length=4, frozen=True, max_length=128)
    team_id: int = Field(..., frozen=True)
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)
    status: Optional[ProjectStatus] = ProjectStatus.OPEN
    closed_at: Optional[datetime] = Field(default_factory=get_utc_now)
    teams: Optional[List[TeamsOfProject]] = []
    tasks: Optional[List[TasksBase]] = []
    
    @model_validator(mode="before")
    @classmethod
    def validate_unique_task_names(cls, values):
        tasks = values.get("tasks", [])
        task_names = [task["name"] for task in tasks]
        if len(task_names) != len(set(task_names)):
            raise ValueError("Each task in the project must have a unique name.")
        return values

class ProjectCreateRequestSchema(BaseModel):
    name: str = Field(min_length=4, frozen=True, max_length=64)
    description: str = Field(..., min_length=4, frozen=True, max_length=128)
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)
    team_id: int = Field(..., frozen=True)

class ProjectCreateResponseSchema(BaseModel):
    id: int

class GetProjectDetailsRequestSchema(BaseModel):
    id: int

class GetProjectDetailsResponseSchema(BaseModel):
    id: int
    name: str

class AddTaskRequestSchema(BaseModel):
    name: Text = Field(..., min_length=4, frozen=True, max_length=64, description="project name")
    task_name: Text = Field(..., min_length=4, frozen=True, max_length=64, description="task name")
    description: Text = Field(..., min_length=4, frozen=True, max_length=128, description="task description")
    user_id: int
    created_at: datetime = Field(frozen=True, default_factory=get_utc_now)

class AddTaskResponseSchema(TasksBase):
    id: int

class UpdateTaskRequestSchema(BaseModel):
    id: int
    status: TaskStatus

class TeamIdRequestSchema(BaseModel):
    id: int

class ListBoardResponseSchema(BaseModel):
    id: int
    name: Text


