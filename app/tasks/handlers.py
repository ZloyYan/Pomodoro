import time
from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Depends
from typing import Annotated

from app.exceptions import TaskNotFoundException
from app.tasks.schema import TaskSchema, TaskCreateSchema
from app.tasks.repository import TaskRepository
from app.dependency import get_request_user_id, get_tasks_service, get_tasks_repository
from app.tasks.service import TaskService


router = APIRouter(prefix='/task', tags=['task'])  # group API endpoints under "task" tag


def get_tasks_log(tasks_count: int):
    time.sleep(3.0)
    print(f"get {tasks_count} tasks")

@router.get('/all', response_model=list[TaskSchema])  # response_model specifies the expected response data structure. In this case, it's a list of Task objects.
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    background_tasks: BackgroundTasks
    
):
    tasks = await task_service.get_tasks()  # get all tasks from the repository
    background_tasks.add_task(get_tasks_log, tasks_count=len(tasks))  # add a background task to
    return await tasks


@router.post(
    '/', 
    response_model=TaskSchema
)
async def create_task(
    body: TaskCreateSchema, 
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id)
):
    task = await task_service.create_task(body, user_id)
    return task

@router.patch(
    '/{task_id}', 
    response_model=TaskSchema
)
async def update_task(
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    name: str,
    task_id: int, 
    user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.update_task_name(task_id, user_id, name)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)



@router.delete(
    '/{task_id}', 
    status_code=status.HTTP_204_NO_CONTENT  
)
async def delete_task(
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    task_id: int, 
    user_id: int = Depends(get_request_user_id)
    ):
    try: 
        await task_service.delete_task(task_id, user_id)
        return {"detail": "Task deleted"}
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
