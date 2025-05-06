from fastapi.params import Depends
from sqlalchemy.orm import Session

from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService
from db import get_db_session
from cache import get_redis_connection
from service.auth import AuthService


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


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository)
