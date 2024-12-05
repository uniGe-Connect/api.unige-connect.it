import uuid
from datetime import datetime
from sqlmodel import SQLModel


class GroupPublic(SQLModel):
    id: uuid.UUID
    name: str
    topic: str
    description: str
    type: str
    member_count: int
    created_at: datetime


class GroupsPublic(SQLModel):
    data: list[GroupPublic]