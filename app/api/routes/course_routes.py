import uuid

from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, auth_user
from app.controllers.course_controller import course_controller
from app.resources.course_resource import CoursesPublic

router = APIRouter()
@router.get("/courses", response_model=CoursesPublic, dependencies=[Depends(auth_user)])
def index(session: SessionDep) -> CoursesPublic:
    courses = course_controller.get_all(session=session)

    return CoursesPublic(data=courses)