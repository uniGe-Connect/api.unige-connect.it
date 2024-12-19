import uuid
from sqlmodel import SQLModel
from app.models.member_model import MemberTypes


class UserPublic(SQLModel):
    id: uuid.UUID
    name: str
    last_name: str
    email: str

    
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class UserMemberPublic(SQLModel):
    name: str
    last_name: str
    role: MemberTypes


class UsersMemberPublic(SQLModel):
    data: list[UserMemberPublic]
    count: int