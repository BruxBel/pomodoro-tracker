from fastapi import security, HTTPException, Request
from fastapi.params import Depends, Security

from sqlalchemy.ext.asyncio import AsyncSession

from client import GoogleClient
from exceptions import TokenExpiredException
from exceptions.auth import TokenNotCorrectException
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService
from db import get_db_session
from redis import ConnectionError, TimeoutError
from cache import RedisStorage

from service.auth import AuthService

from config import settings


async def get_task_repository(
        db_session: AsyncSession = Depends(get_db_session)
) -> TaskRepository:
    return TaskRepository(db_session=db_session)


async def get_redis_storage(request: Request) -> RedisStorage:

    redis_storage = getattr(request.app.state, 'redis_storage', None)
    if not redis_storage:
        raise HTTPException(500, "Redis storage not initialized")

    try:
        async with redis_storage.connection() as conn:
            await conn.ping()
        return redis_storage
    except (ConnectionError, TimeoutError) as e:
        raise HTTPException(503, "Redis service unavailable") from e


async def get_task_cache(
        redis_storage: RedisStorage = Depends(get_redis_storage)) -> TaskCache:
    return TaskCache(redis_storage=redis_storage)


async def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
        task_cache: TaskCache = Depends(get_task_cache)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) \
        -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=settings)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=google_client
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository,
                       auth_service=auth_service)


reusable_auth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials =
    Security(reusable_auth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenNotCorrectException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_id
