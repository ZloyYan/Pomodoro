from fastapi import Depends, HTTPException, Security, security
import httpx


from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.cache import get_redis_connection
from app.users.auth.client import GoogleClient, YandexClient
from app.exceptions import InvalidTokenException, TokenExpiredException
from app.tasks.repository import TaskCache

from app.tasks.repository import TaskRepository
from app.users.user_profile.repository import UserRepository
from app.infrastructure.database import get_db_session
from app.tasks.service import TaskService
from app.users.auth.service import AuthService
from app.users.user_profile.service import UserService
from settings import Settings

async def get_tasks_repository() -> TaskRepository:
    db_session: AsyncSession = Depends(get_db_session())
    return TaskRepository(db_session=db_session)

async def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)

async def get_tasks_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache_repository: TaskCache = Depends(get_tasks_cache_repository)  # use dependency injection to provide the task cache repository. This way, the task service can use the same repository for both tasks and cache.  # This is a best practice for scalability and maintainability.  # Depends decorator automatically injects the dependency when the function is called.  # In this case, the get_tasks_repository and get_tasks_cache_repository functions
) -> TaskService:
    tasks_repository = get_tasks_repository()
    tasks_cache_repository = get_tasks_cache_repository()
    return TaskService(tasks_repository, tasks_cache_repository)

async def get_user_repository():
    db_session = get_db_session()
    return UserRepository(db_session=db_session)

async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()

async def get_google_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)

async def get_yandex_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),  # use dependency injection to provide
    yandex_client: YandexClient = Depends(get_yandex_client),  # use
) -> AuthService:
    return AuthService(
        user_repository=user_repository, 
        settings=Settings(), 
        google_client=google_client, 
        yandex_client=yandex_client
    )



async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)  # use dependency injection to provide the auth service. This way, the user service can use the same repository for both user and auth.  # This is a best practice for scalability and maintainability.  # Depends decorator automatically injects the dependency when the function is called.  # In this case, the get_user_repository and get_auth_service functions
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


reusable_oauth2 = security.HTTPBearer()

async def get_request_user_id(
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
