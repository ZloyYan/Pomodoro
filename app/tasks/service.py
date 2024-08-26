from dataclasses import dataclass

from app.exceptions import TaskNotFoundException
from app.tasks.repository import TaskRepository, TaskCache
from app.tasks.schema import TaskSchema, TaskCreateSchema



@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self) -> list[TaskSchema]:
        if tasks := await self.task_cache.get_tasks():
            return tasks
        else:
            tasks = await self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks
        
    async def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id)
        new_task = TaskSchema.model_validate(task)
        await self.task_cache.add_task(new_task)
        return new_task
    
    async def update_task_name(self, task_id: int, user_id: int, name: str) -> TaskSchema:
        user_task = await self.task_repository.get_user_task(user_id, task_id)
        if not user_task:
            raise TaskNotFoundException
        updated_task = await self.task_repository.update_task_name(task_id, user_id, name)
        updated_task_schema = TaskSchema.model_validate(updated_task)
        await self.task_cache.delete_task(task_id)
        await self.task_cache.add_task(updated_task_schema)
        return updated_task_schema
    
    async def delete_task(self, task_id: int, user_id: int) -> None:
        user_task = await self.task_repository.get_user_task(user_id, task_id)
        if not user_task:
            raise TaskNotFoundException
        self.task_repository.delete_task(task_id, user_id)
        await self.task_cache.delete_task(task_id)