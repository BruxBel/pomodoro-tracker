from schemas import TaskSchema
from cache import RedisStorage


class TaskCache:
    def __init__(self, redis_storage: RedisStorage):
        self.redis = redis_storage

    async def get_tasks(self) -> list[TaskSchema]:
        """Асинхронно получает все задачи из хеша"""
        async with self.redis.connection() as redis_conn:
            tasks_dict = await redis_conn.hgetall("tasks")
        return [
            TaskSchema.model_validate_json(task_json)
            for task_json in tasks_dict.values()
        ]

    async def add_task(self, task: TaskSchema):
        task_json = task.model_dump_json()
        async with self.redis.connection() as redis_conn:
            await redis_conn.hset("tasks", str(task.id), task_json)

    async def delete_task(self, task_id: int):
        """Удаляет задачу из хеша по ID"""
        async with self.redis.connection() as redis_conn:
            await redis_conn.hdel("tasks", str(task_id))

    async def update_task(self, task: TaskSchema):
        task_json = task.model_dump_json()
        async with self.redis.connection() as redis_conn:
            await redis_conn.hset("tasks", str(task.id), task_json)

    async def set_tasks(self, tasks: list[TaskSchema]):
        """Атомарно заменяет все задачи в хеше 'tasks'"""
        async with self.redis.connection() as redis_conn:
            async with await redis_conn.pipeline() as pipe:
                # Удалить весь хеш
                pipe.delete("tasks")

                # Добавить новые задачи
                for task in tasks:
                    pipe.hset("tasks", task.id, task.model_dump_json())

                await pipe.execute()
