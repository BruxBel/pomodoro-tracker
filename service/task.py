from dataclasses import dataclass

from exceptions import TaskNotFoundException
from repository import TaskRepository, TaskCache
from schemas import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_task(self, task_id: int) -> TaskSchema | None:
        task = self.task_repository.get_task(task_id=task_id)
        return task

    async def get_tasks(self) -> list[TaskSchema]:
        # Пробуем получить из кеша
        if cached_tasks := await self.task_cache.get_tasks():
            return cached_tasks

        # Получаем из репозитория
        tasks = self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]

        # Кешируем результат
        await self.task_cache.set_tasks(tasks_schema)
        return tasks_schema

    async def create_task(
            self,
            body: TaskCreateSchema,
            user_id: int
    ) -> TaskSchema:
        task = self.task_repository.create_task(body, user_id)
        await self.task_cache.add_task(task=task)
        return task

    async def update_task(
            self,
            task_id: int,
            name: str,
            user_id: int
    ) -> TaskSchema:
        task = self.task_repository.get_user_task(user_id=user_id,
                                                  task_id=task_id)
        if not task:
            raise TaskNotFoundException
        updated_task = self.task_repository.update_task(task_id=task_id,
                                                        name=name)
        await self.task_cache.update_task(task=updated_task)
        return updated_task

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id,
                                                  task_id=task_id)
        if not task:
            raise TaskNotFoundException
        await self.task_cache.delete_task(task_id=task_id)
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)
