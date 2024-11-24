import uuid

from sqlmodel import SQLModel

from app.models.group_model import GroupModel


class GroupPublic(GroupModel):
    pass

class GroupsPublic(SQLModel):
    data: list[GroupPublic]