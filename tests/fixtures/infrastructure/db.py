import pytest_asyncio
from src.infrastructure.db import Base
from src.tasks.models import TaskModel, CategoryModel
from src.users.models import UserModel

from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)
from src.infrastructure.config import settings


async_engine = create_async_engine(
    settings.db_url_asyncpg_test,
    echo=True,
    future=True,
    pool_pre_ping=True
)


AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_models(event_loop):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()


@pytest_asyncio.fixture()
async def get_db_session() -> AsyncSession:
    """Асинхронный генератор сессий для Dependency Injection"""
    return AsyncSessionFactory()
