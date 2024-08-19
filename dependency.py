from fastapi import Depends

from cache.accessor import get_redis_connection
from repository.cache_task import TaskCache
from repository.task import TaskRepository
from database import get_db_session
from service.task import TaskService

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)

def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)

def get_tasks_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache_repository: TaskCache = Depends(get_tasks_cache_repository)  # use dependency injection to provide the task cache repository. This way, the task service can use the same repository for both tasks and cache.  # This is a best practice for scalability and maintainability.  # Depends decorator automatically injects the dependency when the function is called.  # In this case, the get_tasks_repository and get_tasks_cache_repository functions
) -> TaskService:
    tasks_repository = get_tasks_repository()
    tasks_cache_repository = get_tasks_cache_repository()
    return TaskService(tasks_repository, tasks_cache_repository)