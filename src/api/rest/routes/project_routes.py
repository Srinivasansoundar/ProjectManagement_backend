from fastapi import APIRouter, Depends,status,Query,Path
from src.core.services import project_service
from src.schemas.project_schemas import (
   CreateProjectRequest,
   ProjectResponse,    
   UpdateProjectRequest,
   ProjectDevelopers
)
from src.api.rest.dependencies.service import get_project_service
from src.api.rest.dependencies.role import require_roles
from src.core.services.project_service import ProjectService
from uuid import UUID
router=APIRouter()

@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_project(
    payload: CreateProjectRequest,
    _=Depends(require_roles("admin")),
    project_service:ProjectService=Depends(get_project_service),
)->ProjectResponse:
    response=await project_service.create_project(payload)
    return response

@router.get(
    "/projects",
    response_model=list[ProjectResponse]
)
async def get_projects(
    _=Depends(require_roles("admin")),
    project_service:ProjectService=Depends(get_project_service)
)->list[ProjectResponse]:
    response=await project_service.get_all_projects()
    return response

@router.get(
    "/projects/manager/{manager_id}",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK
)
async def get_projects_by_manager(
    manager_id: UUID = Path(..., description="Manager ID"),
    _=Depends(require_roles("manager")),
    project_service: ProjectService = Depends(get_project_service)
) -> list[ProjectResponse]:
    response = await project_service.get_projects_by_manager(manager_id)
    return response

@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK
)
async def get_project_by_id(
    project_id:UUID=Path(..., description="Project ID"),
    _=Depends(require_roles("admin","manager")),
    project_service:ProjectService=Depends(get_project_service)
)->ProjectResponse:
    response=await project_service.get_project_by_id(project_id)
    return response

@router.put(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK
)
async def update_project(
    payload:UpdateProjectRequest,
    project_id:UUID=Path(...,description="Project ID"),
    _=Depends(require_roles("admin")),
    project_service:ProjectService=Depends(get_project_service)
)->ProjectResponse:
    response=await project_service.update_project(project_id,payload)
    return response

@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(
    project_id:UUID=Path(...,description="Project Id"),
    _=Depends(require_roles("admin")),
    project_service:ProjectService=Depends(get_project_service)
):
    await project_service.delete_project(project_id)
    return None

@router.patch(
    "/projects/{project_id}/{manager_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK
)
# i think it is not needed
async def assign_manager(
    project_id:UUID=Path(...,description="Project ID"),
    manager_id:UUID=Path(...,description="Manager ID"),
    _=Depends(require_roles("admin")),
    project_service:ProjectService=Depends(get_project_service)
)->ProjectResponse:
    response=await project_service.assign_manager(project_id,manager_id)
    return response

@router.post(
    "/projects/{project_id}/developers",
    status_code=status.HTTP_200_OK
)
async def assign_developer(
    payload:ProjectDevelopers,
    project_id:UUID=Path(...,description="Project ID"),
    _=Depends(require_roles("admin")),
    project_service:ProjectService=Depends(get_project_service)
):
    await project_service.assign_developers(project_id,payload)
    return None

@router.get(
    "/projects/{project_id}/developers",
    response_model=ProjectDevelopers,
    status_code=status.HTTP_200_OK
)
async def get_project_developers(
    project_id:UUID=Path(...,description="Project ID"),
    _=Depends(require_roles("admin","manager")),
    project_service:ProjectService=Depends(get_project_service)
)->ProjectDevelopers:
    response=await project_service.get_project_developers(project_id)
    return response

@router.delete(
    "/projects/{project_id}/developers/{developer_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_developer(
    project_id:UUID=Path(...,description="Project ID"),
    developer_id:UUID=Path(...,description="Developer ID"),
    _=Depends(require_roles("admin")),
    project_service:ProjectService=Depends(get_project_service)
):
    await project_service.remove_developer_from_project(project_id,developer_id)
    return None
