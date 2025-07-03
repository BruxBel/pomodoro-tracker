from contextlib import asynccontextmanager

from redis.asyncio import Redis, ConnectionPool
from redis import ConnectionError, TimeoutError, RedisError
from typing import Optional, AsyncIterator

from config import Settings
from dataclasses import dataclass


@dataclass
class RedisStorage:
    settings: Settings
    _pool: Optional[ConnectionPool] = None

    async def init(self) -> None:
        if self._pool is not None:
            return

        try:
            self._pool = ConnectionPool.from_url(
                url=self.settings.redis_url,
                max_connections=10,
                socket_connect_timeout=5,
                socket_timeout=10,
                retry_on_timeout=True,
                health_check_interval=30,
                decode_responses=False
            )

        except ConnectionError as e:
            # logger.error(f"Redis connection failed: {str(e)}")
            await self._cleanup()
            raise RedisError("Could not connect to Redis server") from e

        except TimeoutError as e:
            # logger.error(f"Redis connection timeout: {str(e)}")
            await self._cleanup()
            raise RedisError("Redis server timeout") from e

        except Exception as e:
            # logger.error(f"Failed to initialize Redis pool: {str(e)}")
            await self._cleanup()
            raise RedisError("Redis initialization failed") from e

    async def _cleanup(self) -> None:
        """Очистка ресурсов при ошибке инициализации"""
        if self._pool:
            try:
                await self._pool.disconnect()
            # except Exception as e:
                # logger.warning(f"Error cleaning up Redis pool: {str(e)}")
            finally:
                self._pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[Redis]:
        if self._pool is None:
            raise RuntimeError("Redis pool not initialized. Call init()")

        conn = None
        try:
            conn = Redis(connection_pool=self._pool)

            try:
                await conn.ping()
            except (ConnectionError, TimeoutError) as e:
                # logger.error(f"Redis connection failed: {str(e)}")
                raise RedisError("Could not connect to Redis") from e

            yield conn

        except RedisError as e:
            # logger.error(f"Redis operation failed: {str(e)}")
            raise RedisError("Redis operation failed") from e
        finally:
            if conn:
                try:
                    await conn.close()
                except Exception as e:
                    # Не поднимаем исключение при закрытии, только логируем
                    print(f"Error closing Redis connection: {str(e)}")

    async def close(self) -> None:
        """Корректно закрывает все подключения."""
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
