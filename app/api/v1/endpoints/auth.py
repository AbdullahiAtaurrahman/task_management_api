from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, UserResponse, Token
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


@router.post("/login", response_model=Token, status_code=status.HTTP_202_OK)
async def user_login(
    service: UserService = Depends(get_user_service),
    form: OAuth2PasswordRequestForm = Depends(),
):

    token = await service.login_user(
        email=form.username,
        password=form.password,
    )

    return token
