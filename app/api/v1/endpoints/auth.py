from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.api.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    data: UserCreate, service: UserService = Depends(get_user_service)
):
    user_data = data.model_dump()

    user = await service.create_user(user_data)

    return user
