from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings


engine = create_engine(settings.db_url_psycopg2)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def get_db_session() -> sessionmaker:
    """Генератор сессий для Dependency Injection"""
    return SessionLocal
