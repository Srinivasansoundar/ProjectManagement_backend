from fastapi import Depends
from src.api.rest.dependencies.repositories import get_project_repository, get_project_members_repository
from src.core.services.project_service import ProjectService
from src.data.repositories.project_repositories import ProjectRepository
from src.data.repositories.project_members_repository import ProjectMembersRepository
from src.data.repositories.task_repository import TaskRepository
from src.core.services.task_service import TaskService
from src.api.rest.dependencies.repositories import get_task_repository
def get_project_service(
    project_repository: ProjectRepository = Depends(get_project_repository),
    project_members_repository: ProjectMembersRepository = Depends(get_project_members_repository)
):
    return ProjectService(project_repository, project_members_repository)

def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository)
):
    return TaskService(task_repository)