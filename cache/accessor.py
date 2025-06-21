import os
from redis.asyncio import Redis, ConnectionPool
from typing import Optional


class RedisStorage:
    """Асинхронный Redis-клиент с пулом подключений."""

    def __init__(self):
        self._pool: Optional[ConnectionPool] = None
        self._redis: Optional[Redis] = None

    async def init(self) -> None:
        """Инициализирует пул подключений Redis."""
        self._pool = ConnectionPool(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            password=os.getenv("REDIS_PASSWORD"),
            # Декодировать ответы в строки (по желанию)
            # decode_responses=True,
            max_connections=10,     # Максимальное количество соединений
        )
        self._redis = Redis(connection_pool=self._pool)

    async def get_connection(self) -> Redis:
        """Возвращает асинхронный клиент Redis."""
        if self._redis is None:
            raise RuntimeError("Redis не инициализирован. "
                               "Вызовите `init()` сначала.")
        return self._redis

    async def close(self) -> None:
        """Закрывает пул подключений Redis."""
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
            self._redis = None


# Глобальный экземпляр
redis_storage = RedisStorage()
