from fastapi import APIRouter, Depends,status,Path
from src.api.rest.dependencies.role import require_roles
from src.api.rest.dependencies.service import get_task_service
from src.core.services.task_service import TaskService
from src.schemas.task_schemas import(
    CreateTaskRequest,
    TaskResponse,
    UpdateTaskRequest,
    TaskStatusRequest
)

from uuid import UUID
router=APIRouter()

@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    task:CreateTaskRequest,
    _=Depends(require_roles("manager")),
    task_service: TaskService = Depends(get_task_service)
)->TaskResponse:
    res=await task_service.create_task(task)
    return res

@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
async def update_task(
    task_id: UUID,
    task: UpdateTaskRequest,
    _=Depends(require_roles("manager")),
    task_service: TaskService = Depends(get_task_service)
)->TaskResponse:
    res=await task_service.update_task(task_id, task)
    return res

@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: UUID,
    _=Depends(require_roles("manager")),
    task_service: TaskService = Depends(get_task_service)
):
    await task_service.delete_task(task_id)

@router.get(
    "/tasks/{project_id}",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK
)
async def get_tasks_for_project(
    project_id:UUID=Path(..., description="ID of the project to fetch tasks for"),
    _=Depends(require_roles("manager", "developer")),
    task_service: TaskService = Depends(get_task_service)
):
    res=await task_service.get_tasks_by_project_id(project_id)
    return res

@router.get(
    "/tasks/assigned-to/{user_id}",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK
)
async def get_tasks_assigned_to_user(
    user_id:UUID=Path(..., description="ID of the user to fetch assigned tasks for"),
    _=Depends(require_roles("developer")),
    task_service: TaskService = Depends(get_task_service)
):
    res=await task_service.get_tasks_by_assigned_to(user_id)
    return res

@router.patch(
    "/tasks/{task_id}/assign/{user_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
async def assign_task(
    task_id: UUID,
    user_id: UUID,
    _=Depends(require_roles("manager")),
    task_service: TaskService = Depends(get_task_service)
)->TaskResponse:
    res=await task_service.assign_task(task_id, user_id)
    return res

@router.patch(
    "/tasks/{task_id}/remove/{user_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
async def remove_task_assignment(
    task_id: UUID,
    user_id: UUID,
    _=Depends(require_roles("manager")),
    task_service: TaskService = Depends(get_task_service)
)->TaskResponse:
    res=await task_service.remove_task_assignment(task_id)
    return res


@router.patch(
    "/tasks/{task_id}/update_status",
    response_model=TaskResponse
)
async def update_task_status(
    task_id: UUID,
    status: TaskStatusRequest,
    _=Depends(require_roles("manager", "developer")),
    task_service: TaskService = Depends(get_task_service)
)->TaskResponse:
    res=await task_service.update_task_status(task_id, status)
    return res