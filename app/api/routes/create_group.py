from fastapi import APIRouter
# from models import Group  # Import the Group model
from pydantic import BaseModel

router = APIRouter()

# Define the Pydantic model for input data
class GroupCreate(BaseModel):
    name: str
    topic: str
    description: str
    type: str
    owner_id: int

@router.post("/groups/create-group")
def create_group(data: GroupCreate) -> dict[str, int]:
    """
    Create a new group
    """
    # Create an instance of the Group model and populate it with data
    # new_group = Group(
    #     name=data.name,
    #     topic=data.topic,
    #     description=data.description,
    #     type=data.type,
    #     owner_id=data.owner_id
    # )

    # Add the new group to the session and commit
    # db.add(new_group)
    # db.commit()

    # # Refresh the object to get the generated ID
    # db.refresh(new_group)

    # Return the ID of the newly created group
    # return {"id": new_group.id}
    return {'id': 5}
