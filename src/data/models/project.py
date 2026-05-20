from sqlalchemy import Integer,Text,String,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from sqlalchemy import Enum as SQLEnum
import uuid
from src.data.models.base import Base
from src.data.models.user import User
# note this import is required to import error because of ForeignKey in project model which references user model and vice versa.
# SQLAlchemy will automatically convert PostgreSQL UUID values into Python UUID objects instead of strings.

# because we want enum members to behave like strings.if not type will be enum type
class ProjectStatus(str,Enum):
    ONGOING="ongoing"
    COMPLETED="completed"

class Project(Base):
    __tablename__="projects"
    id:Mapped[UUID]=mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
    description:Mapped[str]=mapped_column(Text,nullable=True)
    status:Mapped[ProjectStatus]=mapped_column(SQLEnum(ProjectStatus),nullable=False,default=ProjectStatus.ONGOING)
    manager_id:Mapped[UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=True)
    created_by:Mapped[UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)

    