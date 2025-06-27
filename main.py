from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from handlers import routers
from cache import RedisStorage

from config import settings


# Должен быть определен ДО создания FastAPI приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_storage = RedisStorage(settings=settings)
    await redis_storage.init()
    app.state.redis_storage = redis_storage  # type: ignore[attr-defined]

    yield  # Здесь приложение работает

    await redis_storage.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)
