from redis.asyncio import Redis
from schemas import TaskSchema
import json


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskSchema]:
        """Асинхронно получает список задач из Redis"""
        tasks_json = await self.redis.lrange("tasks", 0, -1)
        return [TaskSchema.model_validate(json.loads(task))
                for task in tasks_json]

    async def add_task(self, task: TaskSchema):
        task_json = task.model_dump_json()
        await self.redis.rpush("tasks", task_json)

    async def set_tasks(self, tasks: list[TaskSchema]):
        """Асинхронно сохраняет список задач в Redis"""
        tasks_json = [task.model_dump_json() for task in tasks]
        await self.redis.delete("tasks")  # Очищаем перед записью
        await self.redis.rpush("tasks", *tasks_json)
