import uuid
from sqlmodel import SQLModel
from app.models.user_model import UserBaseModel


class CourseTeacherPublic(SQLModel):
    course_id: uuid.UUID
    user_id: uuid.UUID
