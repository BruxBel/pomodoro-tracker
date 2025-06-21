from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from handlers import routers
from cache import redis_storage


# Должен быть определен ДО создания FastAPI приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом приложения:
    - Инициализирует ресурсы при старте
    - Освобождает ресурсы при завершении
    """
    # Инициализация Redis
    await redis_storage.init()
    yield  # Здесь приложение работает
    # Очистка ресурсов
    await redis_storage.close()

app = FastAPI(lifespan=lifespan)

# Должно быть ДО подключения роутеров
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
for router in routers:
    app.include_router(router)

