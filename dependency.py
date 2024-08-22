from fastapi import Depends, HTTPException, Security, security

from cache.accessor import get_redis_connection
from exceptions import InvalidTokenException, TokenExpiredException
from repository.cache_task import TaskCache
from repository import TaskRepository, UserRepository
from database import get_db_session
from service import TaskService, UserService
from service import AuthService
from settings import Settings

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session=db_session)

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

def get_user_repository():
    db_session = get_db_session()
    return UserRepository(db_session=db_session)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository) 
) -> AuthService:
    user_repository = get_user_repository()
    return AuthService(user_repository=user_repository, settings=Settings())


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)  # use dependency injection to provide the auth service. This way, the user service can use the same repository for both user and auth.  # This is a best practice for scalability and maintainability.  # Depends decorator automatically injects the dependency when the function is called.  # In this case, the get_user_repository and get_auth_service functions
) -> UserService:
    user_repository = get_user_repository()
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()

def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),  # use dependency injection
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except InvalidTokenException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
