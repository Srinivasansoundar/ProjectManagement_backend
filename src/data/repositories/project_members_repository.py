from sqlalchemy.ext.asyncio import AsyncSession
from src.data.models.projectmembers import ProjectMember
from sqlalchemy import select
from uuid import UUID

class ProjectMembersRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def add_developer_to_project(self, project_id: UUID, developer_id: UUID) -> ProjectMember:
        """
        Add a developer to a project.
        
        Args:
            project_id: UUID of the project
            developer_id: UUID of the developer user
            
        Returns:
            ProjectMember instance
        """
        project_member = ProjectMember(
            project_id=project_id,
            user_id=developer_id
        )
        self.db.add(project_member)
        await self.db.flush()
        await self.db.refresh(project_member)
        return project_member

    async def get_project_members(self, project_id: UUID) -> list[ProjectMember]:
        """
        Get all members of a project.
        
        Args:
            project_id: UUID of the project
            
        Returns:
            List of ProjectMember instances
        """
        result = await self.db.execute(
            select(ProjectMember).where(ProjectMember.project_id == project_id)
        )
        return result.scalars().all()

    async def is_developer_in_project(self, project_id: UUID, developer_id: UUID) -> bool:
        """
        Check if a developer is already a member of a project.
        
        Args:
            project_id: UUID of the project
            developer_id: UUID of the developer user
            
        Returns:
            Boolean indicating if developer is in project
        """
        result = await self.db.execute(
            select(ProjectMember).where(
                (ProjectMember.project_id == project_id) & 
                (ProjectMember.user_id == developer_id)
            )
        )
        return result.scalar_one_or_none() is not None

    async def remove_developer_from_project(self, project_id: UUID, developer_id: UUID) -> None:
        """
        Remove a developer from a project.
        
        Args:
            project_id: UUID of the project
            developer_id: UUID of the developer user
        """
        project_member = await self.db.execute(
            select(ProjectMember).where(
                (ProjectMember.project_id == project_id) & 
                (ProjectMember.user_id == developer_id)
            )
        )
        member = project_member.scalar_one_or_none()
        if member:
            await self.db.delete(member)
            await self.db.flush()