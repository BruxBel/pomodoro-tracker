from fastapi import APIRouter, Depends
from repository.task import TaskRepository, get_task_repository


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get("/{task_id}")
def get_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repository)
):
    return repo.get_task(task_id)


@router.get("/")
def get_tasks(
    repo: TaskRepository = Depends(get_task_repository)
):
    return repo.get_tasks()
