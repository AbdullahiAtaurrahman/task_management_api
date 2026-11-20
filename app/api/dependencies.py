from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.task import TaskRepository
from app.services.task import TaskService


def get_task_repository(
    db: AsyncSession = Depends(get_db),
):
    return TaskRepository(db)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
):
    return TaskService(repository)


def get_current_user(
    repository: TaskRepository = Depends(get_task_repository),
):
    return TaskService(repository)
