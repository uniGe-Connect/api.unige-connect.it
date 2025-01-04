import uuid
from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING
from app.models.member_model import MemberModel
from app.models.course_teacher_model import CourseTeacherModel

if TYPE_CHECKING:
    from .group_model import GroupModel
    from .course_model import CourseModel

class UserTypes(str, Enum):
    professor = "professor"
    student = "student"

class UserBaseModel(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    serial_number: str | None = Field(default=None, max_length=255)
    type: UserTypes = Field(default="student")
    created_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class UserModel(UserBaseModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Get the user groups
    groups: List["GroupModel"] = Relationship(back_populates="user")
    members: List["GroupModel"] = Relationship(back_populates="users", link_model=MemberModel)
    courses: List["CourseModel"] = Relationship(back_populates="teacher", link_model=CourseTeacherModel)