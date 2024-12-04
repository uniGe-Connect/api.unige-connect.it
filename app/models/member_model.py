import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class MemberTypes(str, Enum):
    owner = "owner"
    member = "member"

class MemberBaseModel(SQLModel):
    role: MemberTypes = Field(default="member")
    user_id: uuid.UUID = Field(foreign_key="users.id")
    group_id: uuid.UUID = Field(foreign_key="groups.id")
    created_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deleted_at: datetime | None = Field()


class MemberModel(MemberBaseModel, table=True):
    __tablename__ = "members"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

