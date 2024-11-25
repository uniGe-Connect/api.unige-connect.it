import uuid
from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class UserTypes(str, Enum):
    professor = "professor"
    student = "student"


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    serial_number: str | None = Field(default=None, max_length=255)
    type: UserTypes = Field(default="student")
    created_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: datetime = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
