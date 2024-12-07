import uuid
from datetime import datetime
from sqlmodel import SQLModel


class MemberPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    group_id: uuid.UUID
    role: str
    created_at: datetime

class MembersPublic(SQLModel):
    data: list[MemberPublic]