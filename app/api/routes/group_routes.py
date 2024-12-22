import uuid

from requests import session
from sqlmodel import select

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, Any

from app.api.deps import CurrentUser, auth_user, group_owner, SessionDep
from app.controllers.group_controller import group_controller
from app.models.group_model import GroupRequest, GroupModel
from app.models.member_model import MemberTypes
from app.resources.group_resource import GroupPublic, GroupsPublic, MyGroups
from app.controllers.member_controller import member_controller

router = APIRouter()

@router.get("/groups", response_model=GroupsPublic | MyGroups, dependencies=[Depends(auth_user)], )
def index(current_user: CurrentUser, session: SessionDep, member: Optional[str] = Query(None)) -> GroupsPublic | MyGroups:
    if member:
        owned_groups = []
        joined_groups = []
        for group in current_user.members:
            group_public = [GroupPublic(**group.__dict__, is_member = True)]
            if(any(group.id == owned_group.id for owned_group in current_user.groups)):
                owned_groups += group_public
            else:
                joined_groups += group_public
        return MyGroups(owned_groups=owned_groups, joined_groups=joined_groups)

    groups = group_controller.get_multi_ordered(order_by='created_at', order='desc', session=session)
    groups_public = [GroupPublic(**group.__dict__,is_member = any(user.id == current_user.id for user in group.users)) for group in groups]
    return GroupsPublic(data=groups_public, count=len(groups_public))


@router.get("/groups/count")
def count(session: SessionDep) -> Any:
    return group_controller.get_count(session=session)


@router.get("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)], )
def show(_id: uuid.UUID, session: SessionDep) -> GroupPublic:
    group = group_controller.get(id=_id, session=session)
    return group


@router.post("/groups", response_model=GroupPublic)
def store(request: GroupRequest, session: SessionDep, current_user: CurrentUser) -> GroupPublic:
    request.owner_id = current_user.id
    group = group_controller.create(obj_in=request, session=session)
    member_controller.create_member(
        user_id=current_user.id,
        group_id=group.id,
        role=MemberTypes.owner,
        session=session

    )

    session.refresh(group)
    return GroupPublic(**group.__dict__, is_member=True)


@router.put("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)])
def update(_id: uuid.UUID, session: SessionDep) -> GroupPublic:
    return group_controller.get(id=_id, session=session)


@router.delete("/groups/{_id}", response_model=GroupPublic)
def destroy(_id: uuid.UUID, session: SessionDep, group: GroupModel = Depends(group_owner)) -> GroupPublic:
    return group_controller.remove(id=group.id, session=session)

@router.put("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)])
def update(_id: uuid.UUID, session: SessionDep, request: GroupRequest, group: GroupModel = Depends(group_owner)) -> GroupPublic:
    try:
        updated_group = group_controller.update(obj_current=group, obj_new=request, session=session)
        return GroupPublic(**updated_group.__dict__, is_member=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))