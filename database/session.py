from os import environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


load_dotenv()
sqlite_db_name = environ.get("SQLITE_DB_NAME", "database.db")

engine = create_engine(f"sqlite:///{sqlite_db_name}")
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def get_db_session() -> sessionmaker:
    """Генератор сессий для Dependency Injection"""
    return SessionLocal
