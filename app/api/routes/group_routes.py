import uuid

from requests import session
from sqlmodel import select
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional, Any

from app.api.deps import CurrentUser, auth_user, SessionDep
from app.models.group_model import GroupRequest, GroupModel
from app.models.member_model import MemberTypes
from app.resources.group_resource import GroupPublic, GroupsPublic, MyGroups
from app.controllers.group_controller import group_controller
from app.models.user_model import UserModel
from app.controllers.member_controller import member_controller

router = APIRouter()

def group_owner(_id: uuid.UUID, session: SessionDep, current_user: UserModel = Depends(auth_user)) -> GroupModel:
    group = group_controller.get(id=_id, session=session)
    if group.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")
    return group

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
    query = select(GroupModel).where(GroupModel.id == _id).where(GroupModel.deleted_at == None)
    if len(group_controller.get_multi(query=query, session=session)) == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Group not found.")
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
    print()
    return GroupPublic(**group.__dict__, is_member=True)


@router.put("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)])
def update(_id: uuid.UUID, session: SessionDep) -> GroupPublic:
    return group_controller.get(id=_id, session=session)


@router.delete("/groups/{_id}", response_model=GroupPublic)
def update(_id: uuid.UUID, session: SessionDep, group: GroupModel = Depends(group_owner)) -> GroupModel:
    return group_controller.delete_group(
        group=group,
        group_id=_id,
        session=session
    )
