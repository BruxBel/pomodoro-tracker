import pytest_asyncio
from src.infrastructure.db import Base
from src.tasks.models import TaskModel, CategoryModel
from src.users.models import UserModel

from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)
from src.infrastructure.config import settings


async_engine = create_async_engine(
    settings.db_url_asyncpg_test,
    echo=False,
    future=True,
    pool_pre_ping=True
)


AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False
)


@pytest_asyncio.fixture(autouse=True)
async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()


@pytest_asyncio.fixture()
async def get_db_session():
    """Фикстура с явным управлением контекстом сессии"""
    return AsyncSessionFactory()
