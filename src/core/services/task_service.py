from uuid import UUID

from src.data.models.task import Task
from src.schemas.task_schemas import (
    CreateTaskRequest,
    TaskResponse,
    TaskStatusRequest
)
from src.core.exception.custom_exception import (
    DatabaseException,
    ResourceNotFound


)
import logging

logger=logging.getLogger(__name__)
class TaskService:
    def __init__(self,task_repository):
        self.task_repository = task_repository
    async def create_task(self,task_data:CreateTaskRequest)->TaskResponse:
        try:
            task=Task(
                title=task_data.title,
                description=task_data.description,
                project_id=task_data.project_id,
                assigned_to=task_data.assigned_to,
                created_by=task_data.created_by
            )
            resp=await self.task_repository.create_task(task)
            logger.info(f"Task created with id: {resp.id}")
            return TaskResponse(
                id=resp.id,
                title=resp.title,
                description=resp.description,
                status=resp.status,
                project_id=resp.project_id,
                assigned_to=resp.assigned_to,
                created_by=resp.created_by
            )
        except Exception as e:
            logger.error(f"Error occurred while creating task: {e}")
            raise DatabaseException("Failed to create task")
    async def update_task(self, task_id:UUID, task_data:CreateTaskRequest)->TaskResponse:
        try:
            task=await self.task_repository.get_task_by_id(task_id)
            if not task:
                logger.warning(f"Task with id {task_id} not found")
                raise ResourceNotFound("Task not found")
            task_dat=task_data.model_dump(exclude_none=True)
            updated_task=await self.task_repository.update_task(task, task_dat)
            logger.info(f"Task with id {task_id} updated successfully")
            return TaskResponse(
                id=updated_task.id,
                title=updated_task.title,
                description=updated_task.description,
                status=updated_task.status,
                project_id=updated_task.project_id,
                assigned_to=updated_task.assigned_to,
                created_by=updated_task.created_by
            )
        except ResourceNotFound as e:
            logger.warning(f"Resource not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while updating task: {e}")
            raise DatabaseException("Failed to update task")
    async def delete_task(self,task_id:UUID):
        try:
            task=await self.task_repository.get_task_by_id(task_id)
            if not task:
                logger.warning(f"Task with id {task_id} not found")
                raise ResourceNotFound("Task not found")
            await self.task_repository.delete_task(task)
            logger.info(f"Task with id {task_id} deleted successfully")
        except ResourceNotFound as e:
            logger.warning(f"Resource not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while deleting task: {e}")
            raise DatabaseException("Failed to delete task")
        
    async def get_tasks_by_project_id(self, project_id:UUID)->list[TaskResponse]:
        try:
            tasks_result=await self.task_repository.get_tasks_by_project_id(project_id)
            if tasks_result is None or len(tasks_result) == 0:
                logger.warning(f"No tasks found for project id {project_id}")
                return []
            logger.info(f"Fetched {len(tasks_result)} tasks for project id {project_id}")
            return [TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                project_id=task.project_id,
                project_name=project.name,
                assigned_to=task.assigned_to,
                created_by=task.created_by
            ) for task, project in tasks_result]
        except Exception as e:
            logger.error(f"Error occurred while fetching tasks: {e}")
            raise DatabaseException("Failed to fetch tasks")
    
    async def get_tasks_by_assigned_to(self, user_id:UUID)->list[TaskResponse]:
        try:
            tasks_result=await self.task_repository.get_tasks_by_assigned_to(user_id)
            if tasks_result is None or len(tasks_result) == 0:
                logger.warning(f"No tasks found for user id {user_id}")
                return []
            logger.info(f"Fetched {len(tasks_result)} tasks for user id {user_id}")
            return [TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                project_id=task.project_id,
                project_name=project.name,
                assigned_to=task.assigned_to,
                created_by=task.created_by
            ) for task, project in tasks_result]
        except Exception as e:
            logger.error(f"Error occurred while fetching tasks: {e}")
            raise DatabaseException("Failed to fetch tasks")
    
    
    async def assign_task(self, task_id:UUID, user_id:UUID)->TaskResponse:
        try:
            task=await self.task_repository.get_task_by_id(task_id)
            if not task:
                logger.warning(f"Task with id {task_id} not found")
                raise ResourceNotFound("Task not found")
            # task.assigned_to=user_id    
            updated_task=await self.task_repository.update_task(task, {"assigned_to": user_id})
            logger.info(f"Task with id {task_id} assigned to user {user_id} successfully")
            return TaskResponse(
                id=updated_task.id,
                title=updated_task.title,
                description=updated_task.description,
                status=updated_task.status,
                project_id=updated_task.project_id,
                assigned_to=updated_task.assigned_to,
                created_by=updated_task.created_by
            )   
        except ResourceNotFound as e:
            logger.warning(f"Resource not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while assigning task: {e}")
            raise DatabaseException("Failed to assign task")
    
    async def remove_task_assignment(self, task_id:UUID)->TaskResponse:
        try:
            task=await self.task_repository.get_task_by_id(task_id)
            if not task:
                logger.warning(f"Task with id {task_id} not found")
                raise ResourceNotFound("Task not found")
            updated_task=await self.task_repository.update_task(task, {"assigned_to": None})
            logger.info(f"Task with id {task_id} assignment removed successfully")
            return TaskResponse(
                id=updated_task.id,
                title=updated_task.title,
                description=updated_task.description,
                status=updated_task.status,
                project_id=updated_task.project_id,
                assigned_to=updated_task.assigned_to,
                created_by=updated_task.created_by
            )   
        except ResourceNotFound as e:
            logger.warning(f"Resource not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while removing task assignment: {e}")
            raise DatabaseException("Failed to remove task assignment")
    
    async def update_task_status(self, task_id:UUID, status_request:TaskStatusRequest)->TaskResponse:
        try:
            task=await self.task_repository.get_task_by_id(task_id)
            if not task:
                logger.warning(f"Task with id {task_id} not found")
                raise ResourceNotFound("Task not found")
            updated_task=await self.task_repository.update_task(task, {"status": status_request.status})
            logger.info(f"Task with id {task_id} status updated to {status_request.status} successfully")
            return TaskResponse(
                id=updated_task.id,
                title=updated_task.title,
                description=updated_task.description,
                status=updated_task.status,
                project_id=updated_task.project_id,
                assigned_to=updated_task.assigned_to,
                created_by=updated_task.created_by
            )   
        except ResourceNotFound as e:
            logger.warning(f"Resource not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while updating task status: {e}")
            raise DatabaseException("Failed to update task status")