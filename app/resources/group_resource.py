import uuid
from datetime import datetime
from sqlmodel import SQLModel

class GroupPublic(SQLModel):
    id: uuid.UUID
    name: str
    course_name: str
    description: str
    type: str
    member_count: int
    created_at: datetime
    is_member: bool = False


class GroupsPublic(SQLModel):
    data: list[GroupPublic]

class MyGroups(SQLModel):
    owned_groups: list[GroupPublic]
    joined_groups: list[GroupPublic]