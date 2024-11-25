import uuid

from sqlmodel import SQLModel

from app.models.user_model import UserModel


class UserPublic(UserModel):
    _id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
