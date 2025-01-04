import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class MemberPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    group_id: uuid.UUID
    role: str
    created_at: datetime
    deleted_at: Optional[datetime] = None

class MembersPublic(SQLModel):
    data: list[MemberPublic]
    count: int