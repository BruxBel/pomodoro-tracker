from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from db import TaskModel
from schemas import TaskSchema, TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int) -> TaskSchema | None:
        async with self.db_session as session:
            model = (await session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            )).scalar_one_or_none()
        return TaskSchema.model_validate(model) if model else None

    async def get_tasks(self) -> list[TaskSchema]:
        async with self.db_session as session:
            result = await session.execute(select(TaskModel))
            task_models = result.scalars().all()
            return [TaskSchema.model_validate(task) for task in task_models]

    async def get_user_task(self, user_id: int, task_id: int
                            ) -> TaskSchema | None:
        query = (
            select(TaskModel)
            .where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
        )
        async with self.db_session as session:
            result = await session.execute(query)
            task_model = result.scalar_one_or_none()
            return TaskSchema.model_validate(
                task_model) if task_model else None

    async def create_task(self, task: TaskCreateSchema,
                          user_id: int) -> TaskSchema:
        task_model = TaskModel(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        )
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            await session.refresh(task_model)
            return TaskSchema.model_validate(task_model)

    async def update_task(self, task_id: int, name: str) -> TaskSchema:
        async with self.db_session as session:
            result = await session.execute(
                update(TaskModel)
                .where(TaskModel.id == task_id)
                .values(name=name)
                .returning(TaskModel)
            )
            updated_task = result.scalar_one_or_none()

            if updated_task is None:
                raise ValueError(f"Task with id {task_id} not found")

            await session.commit()
            return TaskSchema.model_validate(updated_task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        )
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
