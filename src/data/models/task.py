from sqlalchemy import  ForeignKey,Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column   
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum       
from sqlalchemy import Enum as SQLEnum
import uuid
from src.data.models.base import Base
from src.data.models.user import User
class TaskStatus(str,Enum):
    TODO="todo"
    IN_PROGRESS="in_progress"
    DONE="done"
class Task(Base):
    __tablename__="tasks"
    id:Mapped[UUID]=mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True)
    title:Mapped[str]=mapped_column(String(100),nullable=False)
    description:Mapped[str]=mapped_column(Text,nullable=True)
    status:Mapped[TaskStatus]=mapped_column(SQLEnum(TaskStatus),nullable=False,default=TaskStatus.TODO)
    project_id:Mapped[UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("projects.id"),nullable=False)
    assigned_to:Mapped[UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=True)
    created_by:Mapped[UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)