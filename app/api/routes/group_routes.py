import uuid
from datetime import datetime, timedelta

from sqlmodel import select
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional, Any

from app.api.deps import CurrentUser, auth_user, SessionDep
from app.models.group_model import GroupRequest, GroupModel
from app.models.member_model import MemberTypes, MemberModel
from app.resources.group_resource import GroupPublic, GroupsPublic, MyGroups
from app.controllers.group_controller import group_controller
from app.models.user_model import UserModel, UserTypes
from app.controllers.member_controller import member_controller

router = APIRouter()

def group_owner(_id: uuid.UUID, session: SessionDep, current_user: UserModel = Depends(auth_user)) -> GroupModel:
    group = group_controller.get(id=_id, session=session)
    if group.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")
    return group

@router.get("/groups", response_model=GroupsPublic | MyGroups, dependencies=[Depends(auth_user)], )
def index(current_user: CurrentUser, session: SessionDep, member: Optional[str] = Query(None), teacher: Optional[str] = Query(None)) -> GroupsPublic | MyGroups:
    if member and current_user.type == UserTypes.student:
        owned_groups = []
        joined_groups = []
        for group in current_user.members:
            group_public = [GroupPublic(**group.__dict__, is_member = True, course_name=group.course_name)]
            if(any(group.id == owned_group.id for owned_group in current_user.groups)):
                owned_groups += group_public
            else:
                #it finds the record of MemberModel for the corrent user
                member_record = session.query(MemberModel).filter(
                    MemberModel.group_id == group.id,
                    MemberModel.user_id == current_user.id,
                    MemberModel.deleted_at == None  #only deleted_at null, because it means that the user has no leave the group
                ).first()
                if member_record:
                    joined_groups += group_public
        return MyGroups(owned_groups=owned_groups, joined_groups=joined_groups)
    
    if teacher and current_user.type == UserTypes.professor:
        teacher_groups = [group for course in current_user.courses for group in course.groups]
        return GroupsPublic(data=teacher_groups, count=len(teacher_groups))    


    groups = group_controller.get_multi_ordered(order_by='created_at', order='desc', session=session)
    groups_public = [
        GroupPublic(
            **group.__dict__,
            is_member=session.query(MemberModel).filter(
                MemberModel.group_id == group.id,
                MemberModel.user_id == current_user.id,
                MemberModel.deleted_at == None
            ).first() is not None,
            course_name=group.course_name
        )
        for group in groups
    ]
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
        session=session,
        force=True
    )

    session.refresh(group)
    return GroupPublic(**group.__dict__, is_member=True, course_name=group.course_name)

@router.put("/groups/{_id}", response_model=GroupPublic, dependencies=[Depends(auth_user)])
def update(_id: uuid.UUID, session: SessionDep, request: Optional[GroupRequest] = None, group: GroupModel = Depends(group_owner)) -> GroupPublic:
    if request:
        try:
            if group.created_at != group.updated_at and (datetime.now() - group.updated_at) < timedelta(minutes=10):
                raise HTTPException(status_code=400, detail="You can only update a group every 10 minutes")
            else:
                group.updated_at = datetime.now()
                updated_group = group_controller.update(obj_current=group, obj_new=request, session=session)
                return GroupPublic(**updated_group.__dict__, is_member=True)
        except HTTPException as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        return group_controller.get(id=_id, session=session)
      
@router.delete("/groups/{_id}", dependencies=[Depends(group_owner)])
def destroy(_id: uuid.UUID, session: SessionDep) -> bool:
    group_controller.delete_group(
        group_id=_id,
        session=session
    )
    return True