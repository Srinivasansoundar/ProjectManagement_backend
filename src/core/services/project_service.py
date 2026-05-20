import logging
from src.data.repositories.project_repositories import ProjectRepository
from src.data.repositories.project_members_repository import ProjectMembersRepository
from src.data.models.project import Project, ProjectStatus
from src.schemas.project_schemas import (
    CreateProjectRequest,
    UpdateProjectRequest,
    ProjectResponse,
    ProjectDevelopers
)
from src.core.exception.custom_exception import (
    ValidationException,
    DatabaseException,
    ResourceNotFound,
)

from uuid import UUID
logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, project_repository: ProjectRepository, project_members_repository: ProjectMembersRepository):
        self.project_repository = project_repository
        self.project_members_repository = project_members_repository

    async def create_project(self, project: CreateProjectRequest) -> ProjectResponse:
        
        try:
            # Validate input data
            self._validate_create_project_input(project)
            
            # Create project entity
            project_entity = Project(
                name=project.name.strip(),
                description=project.description.strip() if project.description else None,
                status=project.status,
                manager_id=project.manager_id,
                created_by=project.created_by
            )
            
            # Save to database
            created_project = await self.project_repository.create_project(project_entity)
            
            logger.info(f"Project created successfully: {created_project.id}")
            
            return ProjectResponse(
                id=created_project.id,
                name=created_project.name,
                description=created_project.description,
                status=created_project.status,
                manager_id=created_project.manager_id
            )
            
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"Failed to create project: {str(e)}")
            raise DatabaseException(f"Failed to create project: {str(e)}")
    
    async def get_all_projects(self) -> list[ProjectResponse]:
        try:
            projects=await self.project_repository.get_all_projects()
            return [
                ProjectResponse(
                    id=project.id,
                    name=project.name,
                    description=project.description,
                    status=project.status,
                    manager_id=project.manager_id
                )
                for project in projects
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve projects: {str(e)}")
            raise DatabaseException(f"Failed to retrieve projects: {str(e)}")
            
    async def get_projects_by_manager(self, manager_id: UUID) -> list[ProjectResponse]:
        try:
            projects = await self.project_repository.get_projects_by_manager_id(str(manager_id))
            return [
                ProjectResponse(
                    id=project.id,
                    name=project.name,
                    description=project.description,
                    status=project.status,
                    manager_id=project.manager_id
                )
                for project in projects
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve projects for manager {manager_id}: {str(e)}")
            raise DatabaseException(f"Failed to retrieve projects for manager: {str(e)}")
        
    async def get_project_by_id(self, project_id:UUID) -> ProjectResponse:
        try:
            project=await self.project_repository.get_project_by_id(project_id)
            if not project:
                raise ResourceNotFound("Project not found")
            return ProjectResponse(
                    id=project.id,
                    name=project.name,
                    description=project.description,
                    status=project.status,
                    manager_id=project.manager_id
                )
        except ResourceNotFound:
            raise
        except Exception as e:
            logger.error(f"Failed to retrieve project: {str(e)}")
            raise DatabaseException(f"Failed to retrieve project: {str(e)}")
    
    async def update_project(self, project_id: UUID, update_data: UpdateProjectRequest) -> ProjectResponse:
        """
        Update a project with only the provided fields.
        
        Args:
            project_id: The project ID to update
            update_data: The update request with partial fields
            
        Returns:
            Updated ProjectResponse
            
        Raises:
            ResourceNotFound: If project doesn't exist
            ValidationException: If validation fails
            DatabaseException: If database operation fails
        """
        try:
            # Get existing project
            existing_project = await self.project_repository.get_project_by_id(project_id)
            if not existing_project:
                raise ResourceNotFound(f"Project with id {project_id} not found")
            
            # Get only non-None fields from update request
            update_dict = update_data.model_dump(exclude_none=True)
            
            # Clean string fields
            if "name" in update_dict and update_dict["name"]:
                update_dict["name"] = update_dict["name"].strip()
            if "description" in update_dict and update_dict["description"]:
                update_dict["description"] = update_dict["description"].strip()
            
            # Update project through repository
            updated_project = await self.project_repository.update_project(existing_project, update_dict)
            
            logger.info(f"Project updated successfully: {updated_project.id}")
            
            return ProjectResponse(
                id=updated_project.id,
                name=updated_project.name,
                description=updated_project.description,
                status=updated_project.status,
                manager_id=updated_project.manager_id
            )
        except ResourceNotFound:
            raise
        except Exception as e:
            logger.error(f"Failed to update project: {str(e)}")
            raise DatabaseException(f"Failed to update project: {str(e)}")
   
    async def delete_project(self,project_id:UUID)->None:
        try:
            project=await self.project_repository.get_project_by_id(project_id)
            if not project:
                raise ResourceNotFound("Project not found")
            await self.project_repository.delete_project(project)
            logger.info(f"Project deleted successfully: {project_id}")
        except ResourceNotFound:
            raise
        except Exception as e:
            logger.error(f"Failed to delete project: {str(e)}")
            raise DatabaseException(f"Failed to delete project: {str(e)}")
    async def assign_manager(self, project_id: UUID, manager_id: UUID) -> ProjectResponse:
        try:
            project=await self.project_repository.get_project_by_id(project_id)
            if not project:
                raise ResourceNotFound("Project not found")
            update_data={"manager_id":manager_id}
            updated_project=await self.project_repository.update_project(project,update_data)
            logger.info(f"Manager {manager_id} assigned to project {project_id} successfully")
            return ProjectResponse(
                id=updated_project.id,
                name=updated_project.name,
                description=updated_project.description,
                status=updated_project.status,
                manager_id=updated_project.manager_id
            )
        except ResourceNotFound:
            raise
        except Exception as e:
            logger.error(f"Failed to assign manager to project: {str(e)}")
            raise DatabaseException(f"Failed to assign manager to project: {str(e)}")
    async def assign_developers(self, project_id: UUID, payload: ProjectDevelopers) -> None:
        try:
            project = await self.project_repository.get_project_by_id(project_id)
            if not project:
                raise ResourceNotFound("Project not found")
            
            # Get current developers
            current_members = await self.project_members_repository.get_project_members(project_id)
            current_developer_ids = {member.user_id for member in current_members}
            new_developer_ids = set(payload.developer_ids)
            
            # Remove developers not in the new list
            for developer_id in current_developer_ids:
                if developer_id not in new_developer_ids:
                    await self.project_members_repository.remove_developer_from_project(
                        project_id, developer_id
                    )
            
            # Add developers not in the current list
            for developer_id in new_developer_ids:
                if developer_id not in current_developer_ids:
                    await self.project_members_repository.add_developer_to_project(
                        project_id, developer_id
                    )
            
            logger.info(f"Developers {payload.developer_ids} assigned to project {project_id} successfully")
        except ResourceNotFound:
            raise
        except Exception as e:
            logger.error(f"Failed to assign developers to project: {str(e)}")
            raise DatabaseException(f"Failed to assign developers to project: {str(e)}")

    async def get_project_developers(self, project_id:UUID) ->ProjectDevelopers:
        try:
            project = await self.project_repository.get_project_by_id(project_id)
            if not project:
                raise ResourceNotFound("Project not found")
            
            project_members = await self.project_members_repository.get_project_members(project_id)
            developer_ids = [str(member.user_id) for member in project_members]
            
            logger.info(f"Retrieved developers for project {project_id} successfully")
            return ProjectDevelopers(developer_ids=developer_ids)
        except ResourceNotFound:
            raise
        except Exception as e:
            logger.error(f"Failed to retrieve project developers: {str(e)}")
            raise DatabaseException(f"Failed to retrieve project developers: {str(e)}")
    async def remove_developer_from_project(self, project_id: UUID, developer_id: UUID) -> None:
        try:
            project = await self.project_repository.get_project_by_id(project_id)
            if not project:
                raise ResourceNotFound("Project not found")
            
            is_member = await self.project_members_repository.is_developer_in_project(project_id, developer_id)
            if not is_member:
                raise ResourceNotFound("Developer is not a member of the project")
            
            await self.project_members_repository.remove_developer_from_project(project_id, developer_id)
            
            logger.info(f"Developer {developer_id} removed from project {project_id} successfully")
        except ResourceNotFound:
            raise
        except Exception as e:
            logger.error(f"Failed to remove developer from project: {str(e)}")
            raise DatabaseException(f"Failed to remove developer from project: {str(e)}")
    def _validate_create_project_input(self, project: CreateProjectRequest) -> None:
        """
        Validate project creation input.
        
        Raises:
            ValidationException: If any validation fails
        """
        if not project.name or not project.name.strip():
            raise ValidationException("Project name is required and cannot be empty")
        
        if len(project.name) > 100:
            raise ValidationException("Project name cannot exceed 100 characters")
        
        if project.description and len(project.description) > 500:
            raise ValidationException("Project description cannot exceed 500 characters")
        
        # Validate status
        try:
            ProjectStatus(project.status)
        except ValueError:
            valid_statuses = [status.value for status in ProjectStatus]
            raise ValidationException(
                f"Invalid project status. Valid statuses are: {', '.join(valid_statuses)}"
            )
        
        if not project.created_by:
            raise ValidationException("Created by user ID is required")