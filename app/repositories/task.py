from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tasks(self, user_id: int):
        statement = select(Task).where(Task.user_id == user_id)

        result = await self.db.execute(statement)
        tasks = result.scalars().all()
        return tasks

    async def get_task_by_id(self, task_id: int, user_id: int):

        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)

        result = await self.db.execute(statement)

        task = result.scalar_one_or_none()
        return task

    async def create_task(self, user_id: int, task_data: dict):
        task = Task(**task_data, user_id=user_id)

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def update_task(self, task_id: int, task_data: dict, user_id: int):
        task = await self.get_task_by_id(task_id, user_id)
        if task is None:
            return None

        for key, value in task_data.items():
            setattr(task, key, value)

        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def delete_task(self, task_id: int, user_id: int):
        task = await self.get_task_by_id(task_id, user_id)

        if task is None:
            return False

        await self.db.delete(task)
        await self.db.commit()

        return True
