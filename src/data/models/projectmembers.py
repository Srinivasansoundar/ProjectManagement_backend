from sqlalchemy import  ForeignKey,Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column   
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum       
from sqlalchemy import Enum as SQLEnum
import uuid
from src.data.models.base import Base
from src.data.models.user import User
from src.data.models.project import Project
class ProjectMember(Base):
    __tablename__="project_members"
    id:Mapped[UUID]=mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True)
    project_id:Mapped[UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("projects.id"),nullable=False)
    user_id:Mapped[UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)