from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update

from db import TaskModel
from schemas import TaskSchema, TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id: int) -> TaskSchema | None:
        with self.db_session as session:
            task_model = session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            ).scalar()
            return TaskSchema.model_validate(
                task_model) if task_model else None

    def get_tasks(self) -> list[TaskSchema]:
        with self.db_session as session:
            task_models = session.execute(
                select(TaskModel)
            ).scalars().all()

            return [TaskSchema.model_validate(task) for task in task_models]

    def get_user_task(self, user_id: int, task_id: int) -> TaskSchema | None:
        query = (
            select(TaskModel)
            .where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
        )
        with self.db_session as session:
            task_model: TaskModel = session.execute(query).scalar_one_or_none()
            return TaskSchema.model_validate(
                task_model) if task_model else None

    def create_task(self, task: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_model = TaskModel(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        )
        with self.db_session as session:
            session.add(task_model)
            session.commit()
            session.refresh(task_model)
            return TaskSchema.model_validate(task_model)

    def update_task(self, task_id: int, name: str) -> TaskSchema:
        with self.db_session as session:
            # Обновляем задачу и получаем обновленную запись
            updated_task: TaskModel | None = session.execute(
                update(TaskModel)
                .where(TaskModel.id == task_id)
                .values(name=name)
                .returning(TaskModel)  # Возвращаем всю модель, а не только id
            ).scalar_one_or_none()

            if updated_task is None:
                raise ValueError(f"Task with id {task_id} not found")

            session.commit()  # Явный коммит для гарантии сохранения изменений
            return TaskSchema.model_validate(updated_task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()
