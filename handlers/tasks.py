from fastapi import APIRouter, Depends, status, HTTPException

from repository import TaskRepository
from schemas import TaskSchema, TaskCreateSchema
from dependencies import get_task_repository
from typing import Annotated


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get(path="/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    repo: Annotated[TaskRepository, Depends(get_task_repository)]
):
    task = repo.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.get(path="/", response_model=list[TaskSchema])
async def get_tasks(
    repo: Annotated[TaskRepository, Depends(get_task_repository)]
):
    tasks = repo.get_tasks()
    return tasks


@router.post(path="/", response_model=TaskSchema)
async def create_task(
    task: TaskCreateSchema,
    repo: Annotated[TaskRepository, Depends(get_task_repository)]
):
    return repo.create_task(task)


@router.patch(path="/{task_id}", response_model=TaskSchema)
async def path_task(
    task_id: int,
    name: str,
    repo: Annotated[TaskRepository, Depends(get_task_repository)]
):
    task = repo.update_task(task_id, name)
    return task


@router.delete(path="/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    repo: Annotated[TaskRepository, Depends(get_task_repository)]
):
    if not repo.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return None
