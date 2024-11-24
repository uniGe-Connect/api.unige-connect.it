import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class GroupTypes(str, Enum):
    public_open = "public_open"
    public_closed = "public_closed"
    private = "private"

class GroupModel(SQLModel, table=True):
    __tablename__ = "groups"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    topic: str = Field(max_length=255)
    description: str = Field(max_length=255)
    type: GroupTypes
    owner_id: uuid.UUID
    created_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class GroupRequest(BaseModel):
    name: str
    topic: str
    description: str
    type: GroupTypes
    owner_id: None
