from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, ConfigDict, model_validator, Field, field_validator


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: TaskPriority
    completed: bool = False
    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or contain only whitespace")

        return value

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value):
        if value is not None:
            if value.tzinfo is None:
                raise ValueError("Due date must include timezone information")

            if value <= datetime.now(timezone.utc):
                raise ValueError("Due date must be in the future")

        return value


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
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

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or contain only whitespace")

        return value

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value):
        if value is not None:
            if value.tzinfo is None:
                raise ValueError("Due date must include timezone information")

            if value <= datetime.now(timezone.utc):
                raise ValueError("Due date must be in the future")

        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    priority: TaskPriority
    completed: bool
    due_date: datetime | None = None
    user_id: int
