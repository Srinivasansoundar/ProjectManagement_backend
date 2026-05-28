from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    project_id: UUID
    assigned_to: Optional[UUID] = None
    created_by: UUID
    
    @field_validator('assigned_to', mode='before')
    @classmethod
    def validate_assigned_to(cls, v):
        if v == '' or v == 'null':
            return None
        return v

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus  
    project_id: UUID
    project_name: Optional[str] = None
    assigned_to: Optional[UUID] = None
    created_by: UUID

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_to: Optional[UUID] = None
    
    @field_validator('assigned_to', mode='before')
    @classmethod
    def validate_assigned_to(cls, v):
        if v == '' or v == 'null':
            return None
        return v
class TaskStatusRequest(BaseModel):
    status:TaskStatus