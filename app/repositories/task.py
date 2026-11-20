from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        statement = select(Task)

        result = await self.db.execute(statement)
        tasks = result.scalars().all()
        return tasks

    async def get_task_by_id(self, task_id: int):

        statement = select(Task).where(Task.id == task_id)

        result = await self.db.execute(statement)

        task = result.scalar_one_or_none()
        return task

    async def create(self, task_data: dict, user_id: int):
        task = Task(**task_data, user_id=user_id)

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh()

        return task
