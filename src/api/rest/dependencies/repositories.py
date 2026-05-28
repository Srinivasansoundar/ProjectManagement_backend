
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.clients.postgress_client import get_async_db
from src.data.repositories.project_repositories import ProjectRepository
from src.data.repositories.project_members_repository import ProjectMembersRepository
from src.data.repositories.task_repository import TaskRepository
def get_project_repository(db: AsyncSession = Depends(get_async_db)) -> ProjectRepository:
    return ProjectRepository(db)
def get_project_members_repository(db: AsyncSession = Depends(get_async_db)) -> ProjectMembersRepository:
    return ProjectMembersRepository(db)
def get_task_repository(db: AsyncSession = Depends(get_async_db)):
    return TaskRepository(db)