from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: TaskPriority
    completed: bool = False
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: TaskPriority | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    priority: TaskPriority
    completed: bool
    due_date: datetime | None = None
    user_id: int
