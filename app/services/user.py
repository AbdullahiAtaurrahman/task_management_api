from fastapi import HTTPException, status
from app.core.security import hash_password

from app.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    async def get_user_by_username(self, username: str):
        return await self.repository.get_user_by_username(username)

    async def create_user(self, user_data: dict):
        data = user_data.copy()
        existing_email = await self.repository.get_user_by_email(data["email"])

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        existing_username = await self.repository.get_user_by_username(data["username"])

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username already taken",
            )

        hashed_password = hash_password(data["password"])
        data["hashed_password"] = hashed_password
        data.pop("password")
        user = await self.repository.create_user(data)
        return user
