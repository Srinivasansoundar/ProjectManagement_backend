from sqlalchemy import Integer,String,Text,ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from sqlalchemy import Enum as SQLEnum
import uuid
from src.data.models.base import Base

# as_uuid=true
# "Convert PostgreSQL UUID values into Python UUID objects not strings"
# if not given string can be assinged to uuid

# because we want enum members to behave like strings.if not type will be enum type
class UserRole(str,Enum):
    ADMIN="admin"
    DEVELOPER="developer"
    MANAGER="manager"

class User(Base):
    __tablename__="users"
    id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name:Mapped[str]=mapped_column(String(50),nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password:Mapped[str]=mapped_column(Text,nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    refresh_token:Mapped[str]=mapped_column(Text,nullable=True)
    
