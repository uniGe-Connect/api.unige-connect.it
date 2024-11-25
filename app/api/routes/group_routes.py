import uuid

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional

from sqlmodel import select

from app.api.deps import CurrentUser, auth_user
from app.controllers.group_controller import group_controller
from app.models.group_model import GroupRequest, GroupModel
from app.resources.group_resource import GroupPublic, GroupsPublic

router = APIRouter()


@router.get("/groups", response_model=GroupsPublic, dependencies=[Depends(auth_user)], )
def index(current_user: CurrentUser, owner: Optional[str] = Query(None)) -> GroupsPublic:
    if owner:
        owner = select(GroupModel).where(GroupModel.owner_id == current_user.id)

    groups = group_controller.get_multi(query=owner)

    return GroupsPublic(data=groups, count=len(groups))


@router.get("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)], )
def show(_id: uuid.UUID) -> GroupPublic:
    group = group_controller.get(id=_id)
    return group


@router.post("/groups", response_model=GroupPublic, dependencies=[Depends(auth_user)])
def store(request: GroupRequest, current_user: CurrentUser) -> GroupPublic:
    request.owner_id = current_user.id
    return group_controller.create(obj_in=request)


@router.delete("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)])
def destroy(_id: uuid.UUID, current_user: CurrentUser) -> GroupPublic:
    group = group_controller.get(id=_id)

    if group.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this group")

    return group_controller.remove(id=_id)
