from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    completed: bool


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    completed: bool | None = None
