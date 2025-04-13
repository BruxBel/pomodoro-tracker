from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete

from database import Task, get_db_session
from typing import Sequence


class TaskRepository:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def get_task(self, task_id: int) -> Task | None:
        with self.db_session() as session:
            task: Task = session.execute(
                select(Task).where(Task.id == task_id)).scalar()
        return task

    def get_tasks(self) -> Sequence[Task]:
        with self.db_session() as session:
            tasks: Sequence[Task] = session.execute(select(Task)).scalars().all()
        return tasks

    def create_task(self, task: Task) -> None:
        with self.db_session() as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id: int) -> None:
        query = delete(Task).where(Task.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()


def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)
