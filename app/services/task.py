from app.repositories.task import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_all_tasks(self, user_id: int):
        return await self.repository.get_all_tasks(user_id)

    async def get_task_by_id(self, task_id: int, user_id: int):
        return await self.repository.get_task_by_id(task_id, user_id)

    async def create_task(self, user_id: int, task_data: dict):
        return await self.repository.create_task(user_id, task_data)

    async def update_task(self, task_id: int, task_data: dict, user_id: int):
        return await self.repository.update_task(task_id, task_data, user_id)

    async def delete_task(self, task_id: int, user_id: int):
        return await self.repository.delete_task(task_id, user_id)
