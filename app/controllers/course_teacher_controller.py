from app.controllers.controller import Controller
from app.models.course_teacher_model import CourseTeacherModel


class CourseController(Controller[CourseTeacherModel, CourseTeacherModel, CourseTeacherModel]):
    pass


course_teacher_controller = CourseController(CourseTeacherModel)
