from fastapi import APIRouter, Depends, status, HTTPException

from app.services.task import TaskService
from app.api.dependencies import get_task_service, get_current_user
from app.models.user import User
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):

    result = await service.create_task(user.id, task_data.model_dump())
    return result


@router.get("", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    result = await service.get_all_tasks(user.id)

    return result


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task_by_id(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    result = await service.get_task_by_id(task_id, user.id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return result


@router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def edit_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    task = task_data.model_dump(exclude_unset=True)
    updated_task = await service.update_task(task_id, task, user.id)

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    deleted_task = await service.delete_task(task_id, user.id)
    if not deleted_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return None
