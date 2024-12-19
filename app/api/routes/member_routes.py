import uuid

from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.controllers.member_controller import member_controller
from app.resources.member_resource import MemberPublic
from app.resources.user_resource import UsersMemberPublic


router = APIRouter()

@router.post("/groups/{_id}/members", response_model=MemberPublic)
def index(_id: uuid.UUID, current_user: CurrentUser) -> MemberPublic:
    return member_controller.create_member(
        user_id=current_user.id,
        group_id=_id
    )
    
@router.get("/groups/{_id}/members", response_model=UsersMemberPublic)
def index(_id: uuid.UUID, current_user: CurrentUser) -> UsersMemberPublic:
    return member_controller.get_members(
        user_id=current_user.id,
        group_id=_id
    )