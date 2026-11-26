from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.core.security import hash_password, verify_password, create_access_token

from app.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    async def get_user_by_username(self, username: str):
        return await self.repository.get_user_by_username(username)

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)

    async def create_user(self, user_data: dict):
        data = user_data.copy()
        existing_email = await self.repository.get_user_by_email(data["email"])

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        existing_username = await self.repository.get_user_by_username(data["username"])

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )
        hashed_password = hash_password(data["password"])
        data["hashed_password"] = hashed_password
        data.pop("password")
        try:
            user = await self.repository.create_user(data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or username already registered",
            )

        return user

    async def login_user(self, email: str, password: str):
        user = await self.repository.get_user_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid email or password",
            )
        is_password_valid = verify_password(password, user.hashed_password)

        if not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        user_token = create_access_token(
            {
                "sub": str(user.id),
            }
        )

        return {"access_token": user_token, "token_type": "bearer"}
