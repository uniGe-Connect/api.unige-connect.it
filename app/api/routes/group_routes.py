from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, auth_user
from app.controllers.group_controller import group_controller
from app.models.group_model import GroupRequest
from app.resources.group_resource import GroupPublic, GroupsPublic

router = APIRouter()


@router.get("/groups", response_model=GroupsPublic, dependencies=[Depends(auth_user)], )
def index() -> GroupsPublic:
    groups = group_controller.get_multi()

    return GroupsPublic(data=groups, count=len(groups))


@router.post("/groups", response_model=GroupPublic, dependencies=[Depends(auth_user)])
def store(request: GroupRequest, current_user: CurrentUser) -> GroupPublic:
    request.owner_id = current_user.id
    return group_controller.create(obj_in=request)
