from fastapi import APIRouter, Depends, status

from app.schemas.task import TaskCreate, TaskResponse
from app.services.task import TaskService
from app.api.dependencies import get_task_service
from app.api.dependencies import get_current_user
from app.models.user import User
