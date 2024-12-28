import uuid

from sqlmodel import SQLModel


class CoursePublic(SQLModel):
    id: uuid.UUID
    name: str


class CoursesPublic(SQLModel):
    data: list[CoursePublic]
