import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel

class CourseTeacherModel(SQLModel, table=True):
    __tablename__ = "courses_teachers"
    course_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
