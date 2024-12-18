import uuid
from sqlmodel import SQLModel
from app.models.user_model import UserBaseModel


class CoursePublic(SQLModel):
    id: uuid.UUID
    name: str
    created_at: datetime

class CoursesPublic(SQLModel):
    data: list[CoursePublic]