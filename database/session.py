from os import environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = environ.get("POSTGRES_HOST")
POSTGRES_PORT = environ.get("POSTGRES_PORT")
POSTGRES_DB = environ.get("POSTGRES_DB")


engine = create_engine(f"postgresql+psycopg2://"
                       f"{POSTGRES_USER}:"
                       f"{POSTGRES_PASSWORD}@"
                       f"{POSTGRES_HOST}:"
                       f"{POSTGRES_PORT}/"
                       f"{POSTGRES_DB}")
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def get_db_session() -> sessionmaker:
    """Генератор сессий для Dependency Injection"""
    return SessionLocal
