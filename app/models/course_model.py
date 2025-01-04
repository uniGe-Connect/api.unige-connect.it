import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from app.models.course_teacher_model import CourseTeacherModel

if TYPE_CHECKING:
    from .group_model import GroupModel
    from .user_model import UserModel


class CourseBaseModel(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deleted_at: datetime | None = Field()


class CourseModel(CourseBaseModel, table=True):
    __tablename__ = "courses"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    groups: List["GroupModel"] = Relationship(back_populates="course")
    teacher: List["UserModel"] = Relationship(back_populates="courses", link_model=CourseTeacherModel)
