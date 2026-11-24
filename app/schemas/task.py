from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, model_validator


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

    @model_validator(mode="before")
    @classmethod
    def reject_null_required_fields(cls, data):
        if isinstance(data, dict):
            required_fields = ["title", "priority", "completed"]

            for field in required_fields:
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null")

        return data


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    priority: TaskPriority
    completed: bool
    due_date: datetime | None = None
    user_id: int
