from fastapi import APIRouter
from app.models import Group
from typing import Any
from app.api.deps import SessionDep, CurrentUser
from sqlmodel import func, select

router = APIRouter()

@router.post("/groups/create-group")
def create_group(data: Group, session: SessionDep) -> dict[str, int]:
    """
    Create new group.
    """
    new_group = Group.model_validate(data)

    session.add(new_group)
    session.commit()
    session.refresh(new_group)
    
    return {"id": new_group.id}

@router.get("/groups/get-your-groups")
def get_owned_groups(session: SessionDep) -> Any:
    """
    Retrieve owned groups.
    """
    
    statement = select(Group).where(Group.owner_id == 1)
    groups = session.exec(statement).all()

    # Convert each group ORM object to a dictionary (serialization)
    group_list = []
    for group in groups:
        group_dict = {
            'id': group.id,
            'name': group.name,
            'topic': group.topic,
            'description': group.description,
            'type': group.type,
        }
        group_list.append(group_dict)
    return group_list  # Return a list of dictionaries
    # return session.select(Group).where(Group.owner_id == current_user.id)
    
@router.get("/groups/get-groups-num")
def get_groups_num(session: SessionDep) -> int:
    """
    Retrieve group count.
    """
    
    statement = select(func.count()).select_from(Group)
    count = session.exec(statement).all()
    return count[0]

@router.delete("/groups/{group_id}")
def delete_group(group_id: int, session: SessionDep) -> dict[str, str]:
    """
    Delete a group by its ID by marking it as deleted.
    """

    statement = select(Group).where(Group.id == group_id)
    group = session.exec(statement).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="There is no group with the provided id")
    
    group.is_deleted = True
    session.commit()
    return {"message": "Group deleted successfully"}

@router.get("/groups/{group_id}")
def get_group(group_id: int, session: SessionDep) -> Any:
    """
    Fetch a group by its ID.
    """

    statement = select(Group).where(Group.id == group_id)
    group = session.exec(statement).first()
    if group.is_deleted:
        raise HTTPException(status_code=404, detail="This group is deleted")

    return group
