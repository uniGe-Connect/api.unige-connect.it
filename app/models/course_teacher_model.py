import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel

class CourseTeacherBaseModel(SQLModel):
    course_id: uuid.UUID = Field(foreign_key="courses.id")
    user_id: uuid.UUID = Field(foreign_key="users.id")

class CourseTeacherModel(CourseTeacherBaseModel, table=True):
    __tablename__ = "courses_teachers"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
