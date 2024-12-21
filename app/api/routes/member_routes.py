import uuid

from fastapi import APIRouter

from app.api.deps import CurrentUser, SessionDep
from app.controllers.member_controller import member_controller
from app.resources.member_resource import MemberPublic
from app.resources.user_resource import UsersMemberPublic


router = APIRouter()

@router.post("/groups/{_id}/members", response_model=MemberPublic)
def index(_id: uuid.UUID, current_user: CurrentUser, session: SessionDep) -> MemberPublic:
    return member_controller.create_member(
        user_id=current_user.id,
        group_id=_id,
        session=session
    )

@router.put("/groups/{_id}/members", response_model=MemberPublic)
def index(_id: uuid.UUID, current_user: CurrentUser,  session: SessionDep) -> MemberPublic:
    return member_controller.member_leave(
        user_id=current_user.id,
        group_id=_id,
        session=session
    )
    
@router.get("/groups/{_id}/members", response_model=UsersMemberPublic)
def index(_id: uuid.UUID, current_user: CurrentUser, session: SessionDep) -> UsersMemberPublic:
    return member_controller.get_members(
        user_id=current_user.id,
        group_id=_id,
        session=session
    )