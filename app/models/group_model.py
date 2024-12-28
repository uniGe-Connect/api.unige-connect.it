import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from sqlmodel import Relationship
from typing import List, TYPE_CHECKING
from app.models.member_model import MemberModel
from app.models.course_model import CourseModel

if TYPE_CHECKING:
    from .user_model import UserModel

class GroupTypes(str, Enum):
    public_open = "public_open"
    public_closed = "public_closed"
    private = "private"

    
class GroupBaseModel(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    course_id: uuid.UUID = Field(foreign_key="courses.id")
    description: str | None = Field(default=None)
    type: GroupTypes = Field(default="public_open")
    owner_id: uuid.UUID = Field(foreign_key="users.id")
    member_count: int = Field(default=0)
    created_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class GroupModel(GroupBaseModel, table=True):
    __tablename__ = "groups"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Get the owner of the group
    user: "UserModel" = Relationship(back_populates="groups")
    course: "CourseModel" = Relationship(back_populates="groups")
    users: List["UserModel"] = Relationship(back_populates='groups', link_model=MemberModel)

    @property
    def course_name(self):
        return self.course.name


class GroupRequest(BaseModel):
    name: str
    course_id: uuid.UUID
    description: str = Field(max_length=300)
    type: GroupTypes
    owner_id: uuid.UUID = Field(default=None)
