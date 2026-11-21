from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.services.task import TaskService
from app.services.user import UserService


def get_task_repository(
    db: AsyncSession = Depends(get_db),
):
    return TaskRepository(db)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
):
    return TaskService(repository)


def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


def get_user_service(repository: UserRepository = Depends(get_user_repository)):
    return UserService(repository)
