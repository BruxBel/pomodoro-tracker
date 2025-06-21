from fastapi import APIRouter, Depends, status, HTTPException

from exceptions import TaskNotFoundException
from repository import TaskRepository
from service import TaskService
from schemas import TaskSchema, TaskCreateSchema
from dependencies import get_task_repository, get_task_service, \
    get_request_user_id
from typing import Annotated


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get(path="/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    repo: Annotated[TaskService, Depends(get_task_service)]
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
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return await task_service.get_tasks()


@router.post(path="/", response_model=TaskSchema)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    task = await task_service.create_task(body, user_id)
    return task


@router.patch(path="/{task_id}", response_model=TaskSchema)
async def path_task(
    task_id: int,
    name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        task = task_service.update_task(task_id=task_id,
                                        name=name,
                                        user_id=user_id)
        return task
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )


@router.delete(path="/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
