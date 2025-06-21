from dataclasses import dataclass

from exceptions import TaskNotFoundException
from repository import TaskRepository, TaskCache
from schemas import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_task(self, task_id: int) -> TaskSchema | None:
        task = self.task_repository.get_task(task_id=task_id)
        return task

    def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks

    def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task = self.task_repository.create_task(body, user_id)
        return task

    def update_task(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = self.task_repository.get_user_task(user_id=user_id,
                                                  task_id=task_id)
        if not task:
            raise TaskNotFoundException
        updated_task = self.task_repository.update_task(task_id=task_id,
                                                        name=name)
        return updated_task

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id,
                                                  task_id=task_id)
        if not task:
            raise TaskNotFoundException
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)
