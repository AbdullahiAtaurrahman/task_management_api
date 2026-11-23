from fastapi import APIRouter, Depends, status

from app.services.task import TaskService
from app.api.dependencies import get_task_service, get_current_user
from app.models.user import User
from app.schemas.task import TaskResponse, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):

    result = await service.create_task(user.id, task_data.model_dump())
    return result


@router.get(response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    result = await service.get_all_tasks(user)

    return result
