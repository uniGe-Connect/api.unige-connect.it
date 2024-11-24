from app.controllers.controller import Controller
from app.models.group_model import GroupModel, GroupRequest


class GroupController(Controller[GroupModel, GroupRequest, GroupModel]):
    pass


group_controller = GroupController(GroupModel)
