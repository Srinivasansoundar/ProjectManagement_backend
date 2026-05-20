from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.data.models.task import Task
from src.data.models.project import Project
from sqlalchemy.ext.asyncio import AsyncSession
class TaskRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
    async def create_task(self, task_data:Task):
        self.db.add(task_data)
        await self.db.flush()
        await self.db.refresh(task_data)
        return task_data
    async def get_task_by_id(self, task_id):
        result=await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
    async def update_task(self, task:Task, task_data:dict):
        for key, value in task_data.items():
            setattr(task, key, value)
        await self.db.flush()
        await self.db.refresh(task)
        return task
    async def delete_task(self,task:Task):
        await self.db.delete(task)
        await self.db.flush()
    async def get_tasks_by_project_id(self, project_id):
        result=await self.db.execute(
            select(Task, Project).join(Project, Task.project_id == Project.id).where(Task.project_id == project_id)
        )
        return result.all()
    
    async def get_tasks_by_assigned_to(self, user_id):
        result=await self.db.execute(
            select(Task, Project).join(Project, Task.project_id == Project.id).where(Task.assigned_to == user_id)
        )
        return result.all()