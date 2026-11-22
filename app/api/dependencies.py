from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.database import get_db
from app.models import User
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.services.task import TaskService
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_task_repository(
    db: AsyncSession = Depends(get_db),
):
    return TaskRepository(db)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
):
    return TaskService(repository)


def get_user_repository(
    db: AsyncSession = Depends(get_db),
):
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
):
    return UserService(repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> User:

    try:
        payload = decode_access_token(token)

        user_id = int(payload.get("sub"))

    except (InvalidTokenError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
