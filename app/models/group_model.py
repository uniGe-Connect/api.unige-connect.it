import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from app.models.user_model import UserModel
from sqlmodel import Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_model import UserModel


class GroupTypes(str, Enum):
    public_open = "public_open"
    public_closed = "public_closed"
    private = "private"

    
class GroupBaseModel(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    topic: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)
    type: GroupTypes = Field(default="public_open")
    owner_id: uuid.UUID = Field(foreign_key="users.id")
    member_count: int = Field(default=1)
    created_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class GroupModel(GroupBaseModel, table=True):
    __tablename__ = "groups"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Get the owner of the group
    user: UserModel = Relationship(back_populates="groups")


class GroupRequest(BaseModel):
    name: str
    topic: str
    description: str = Field(max_length=300)
    type: GroupTypes
    owner_id: uuid.UUID = Field(default=None)
