from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from src.infrastructure.db import async_engine
from src.infrastructure.cache import RedisStorage
from src.infrastructure.config import settings

from src.auth.routes import router as auth_router
from src.users.routes import router as users_router
from src.tasks.routes import router as tasks_router


# Должен быть определен ДО создания FastAPI приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_storage = RedisStorage(settings=settings)
    await redis_storage.init()
    app.state.redis_storage = redis_storage  # type: ignore[attr-defined]

    yield  # Здесь приложение работает

    await async_engine.dispose()

    await redis_storage.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
