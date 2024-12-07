import uuid

from fastapi import APIRouter, Depends, Query
from typing import Optional, Any

from sqlmodel import select

from app.api.deps import CurrentUser, auth_user, group_owner
from app.controllers.group_controller import group_controller
from app.models.group_model import GroupRequest, GroupModel
from app.resources.group_resource import GroupPublic, GroupsPublic

router = APIRouter()


@router.get("/groups", response_model=GroupsPublic, dependencies=[Depends(auth_user)], )
def index(current_user: CurrentUser, owner: Optional[str] = Query(None)) -> GroupsPublic:
    if owner:
        owner = select(GroupModel).where(GroupModel.owner_id == current_user.id)

    groups = group_controller.get_multi(query=owner)
    groups_public = [GroupPublic(**group.__dict__,is_member = any(user.id == CurrentUser.id for user in group.users)) for group in groups]
    return GroupsPublic(data=groups_public, count=len(groups_public))


@router.get("/groups/count")
def count() -> Any:
    return group_controller.get_count()


@router.get("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)], )
def show(_id: uuid.UUID) -> GroupPublic:
    group = group_controller.get(id=_id)
    return group


@router.post("/groups", response_model=GroupPublic)
def store(request: GroupRequest, current_user: CurrentUser) -> GroupPublic:
    request.owner_id = current_user.id
    return group_controller.create(obj_in=request)


@router.put("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)], )
def update(_id: uuid.UUID) -> GroupPublic:
    group = group_controller.get(id=_id)
    return group


@router.delete("/groups/{_id}", response_model=GroupPublic)
def destroy(_id: uuid.UUID, group: GroupModel = Depends(group_owner)) -> GroupPublic:
    return group_controller.remove(id=group.id)
