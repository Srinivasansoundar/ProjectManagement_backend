from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: str = Field(None, max_length=500, description="Project description")
    status: str = Field(default="ongoing", description="Project status")
    manager_id:Optional[UUID] = Field(default=None, description="Manager user ID")
    created_by: UUID = Field(..., description="User ID who created the project")


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    status: str
    manager_id: Optional[UUID] = None

class UpdateProjectRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")
    status: Optional[str] = Field(None, description="Project status")
    manager_id: Optional[UUID] = Field(default=None, description="Manager user ID")

class ProjectDevelopers(BaseModel):
    developer_ids: list[UUID]