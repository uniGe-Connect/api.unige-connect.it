from app.controllers.controller import Controller
from app.models.course_model import CourseModel


class CourseController(Controller[CourseModel, CourseModel, CourseModel]):
    pass


course_controller = CourseController(CourseModel)
