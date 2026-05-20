from sqlalchemy.ext.asyncio import AsyncSession
from src.data.models.project import Project, ProjectStatus
from sqlalchemy import select

# you should usually pass SQLAlchemy models (ORM models), not Pydantic models.
class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, project: Project) -> Project:
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def get_all_projects(self) -> list[Project]:
        result = await self.db.execute(select(Project))
        return result.scalars().all()

    async def get_project_by_id(self, project_id: str) -> Project:
        result = await self.db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()
        
    async def get_projects_by_manager_id(self, manager_id: str) -> list[Project]:
        result = await self.db.execute(select(Project).where(Project.manager_id == manager_id))
        return result.scalars().all()
    
    async def delete_project(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.flush()
        
    async def update_project(self, project: Project, update_data: dict) -> Project:
        for field, value in update_data.items():
            if value is not None:
                setattr(project, field, value)
        
        await self.db.flush()
        await self.db.refresh(project)
        return project

    