import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel



class GroupPublic(SQLModel):
    id: uuid.UUID
    name: str
    topic: str
    description: str
    type: str
    member_count: int
    created_at: datetime
    updated_at: datetime
    is_member: bool = False
    deleted_at: datetime | None = Field()


class GroupsPublic(SQLModel):
    data: list[GroupPublic]

class MyGroups(SQLModel):
    owned_groups: list[GroupPublic]
    joined_groups: list[GroupPublic]