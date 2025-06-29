from fastapi import security, HTTPException
from fastapi.params import Depends, Security
from sqlalchemy.orm import Session

from client import GoogleClient
from exceptions import TokenExpiredException
from exceptions.auth import TokenNotCorrectException
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService
from db import get_db_session
from cache import get_redis_connection
from service.auth import AuthService

from config import settings


def get_task_repository(db_session: Session = Depends(get_db_session)) \
        -> TaskRepository:
    return TaskRepository(db_session=db_session)


def get_task_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
        task_cache: TaskCache = Depends(get_task_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


def get_user_repository(db_session: Session = Depends(get_db_session)) \
        -> UserRepository:
    return UserRepository(db_session=db_session)


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=settings)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=google_client
    )


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository,
                       auth_service=auth_service)


reusable_auth2 = security.HTTPBearer()


def get_request_user_id(
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
