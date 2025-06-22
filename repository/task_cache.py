from redis.asyncio import Redis
from schemas import TaskSchema
import json


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskSchema]:
        """Асинхронно получает все задачи из хеша"""
        tasks_dict = await self.redis.hgetall("tasks")
        return [
            TaskSchema.model_validate_json(task_json)
            for task_json in tasks_dict.values()
        ]

    async def add_task(self, task: TaskSchema):
        task_json = task.model_dump_json()
        await self.redis.hset("tasks", str(task.id), task_json)

    async def delete_task(self, task_id: int):
        """Удаляет задачу из хеша по ID"""
        await self.redis.hdel("tasks", str(task_id))

    async def update_task(self, task: TaskSchema):
        task_json = task.model_dump_json()
        await self.redis.hset("tasks", str(task.id), task_json)

    async def set_tasks(self, tasks: list[TaskSchema]):
        """Атомарно заменяет все задачи в хеше 'tasks'"""
        async with await self.redis.pipeline() as pipe:
            # Удалить весь хеш
            pipe.delete("tasks")

            # Добавить новые задачи
            for task in tasks:
                pipe.hset("tasks", task.id, task.model_dump_json())

            await pipe.execute()
