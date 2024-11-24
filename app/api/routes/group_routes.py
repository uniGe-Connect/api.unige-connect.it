from fastapi import APIRouter, Depends
from typing import Any
from sqlmodel import Session

from app.controllers.group_controller import group_controller
from app.models.group_model import GroupRequest
from app.core.db import get_session
from app.resources.group_resource import GroupPublic, GroupsPublic

router = APIRouter()


@router.get("/groups", response_model=GroupsPublic)
def index() -> Any:
    groups = group_controller.get_multi()

    return GroupsPublic(data=groups, count=len(groups))


@router.post("/groups", response_model=GroupPublic)
def store(request: GroupRequest) -> Any:
    request.owner_id = 'b25a991f-1f3b-4af9-99db-65502a0245d0'
    # TODO: Add owner_id to request
    return group_controller.create(obj_in=request)
