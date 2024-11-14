from fastapi import APIRouter
from pydantic import BaseModel
from app.models import Group, GroupType
from app.api.deps import SessionDep
from fastapi import Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter()

# Define the Pydantic model for input data
# class GroupCreate(BaseModel):
#     name: str
#     topic: str
#     description: str
#     type: str
#     owner_id: int

@router.post("/ciao")
def create_group(data: Group, session: SessionDep) -> dict[str, int]:
    """
    Create new group.
    """
    new_group = Group.model_validate(data)
    """
    Create a new group
    """
    # Create an instance of the Group model and populate it with data
    new_group = Group(
        name=data.name,
        topic=data.topic,
        description=data.description,
        type=GroupType.public_closed,
        owner_id=data.owner_id
    )

    # Add the new group to the session and commit
    session.add(new_group)
    session.commit()
    session.refresh(new_group)
    # # Refresh the object to get the generated ID
    # db.refresh(new_group)

    # Return the ID of the newly created group
    return {"id": new_group.id}
    # return {'id': 5}

# @router.get("/groups/get-your-groups")
# def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
#     """
#     Retrieve users.
#     """

#     count_statement = select(func.count()).select_from(User)
#     count = session.exec(count_statement).one()

#     statement = select(User).offset(skip).limit(limit)
#     users = session.exec(statement).all()

#     return UsersPublic(data=users, count=count)