from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_username(self, username: str):
        statement = select(User).where(User.username == username)
        result = await self.db.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def create_user(self, user_data: dict):
        user = User(**user_data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user
