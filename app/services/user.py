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
        hashed_password = hash_password(data["password"])
        data["hashed_password"] = hashed_password
        data.pop("password")
        user = await self.repository.create_user(data)
        return user
