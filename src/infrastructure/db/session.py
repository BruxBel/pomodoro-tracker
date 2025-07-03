from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)
from typing import AsyncGenerator
from config import settings


async_engine = create_async_engine(
    settings.db_url_asyncpg,
    echo=True,
    future=True,
    pool_pre_ping=True
)


AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """Асинхронный генератор сессий для Dependency Injection"""
    async with AsyncSessionFactory() as session:
        yield session
