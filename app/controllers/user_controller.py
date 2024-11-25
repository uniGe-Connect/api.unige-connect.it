from app.controllers.controller import Controller
from app.models.user_model import UserModel


class UserController(Controller[UserModel, UserModel, UserModel]):
    pass


user_controller = UserController(UserModel)
