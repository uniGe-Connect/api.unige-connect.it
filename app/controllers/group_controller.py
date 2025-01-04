import uuid
from app.controllers.controller import Controller
from app.models.group_model import GroupModel, GroupRequest
from app.models.member_model import MemberModel
from app.resources.group_resource import GroupPublic
from app.api.deps import SessionDep
from datetime import datetime
from sqlalchemy import select, update
from fastapi import HTTPException, status

class GroupController(Controller[GroupModel, GroupRequest, GroupModel]):

    def delete_group(self, group: GroupModel, group_id: uuid.UUID, session: SessionDep) -> GroupPublic:
        # Check if group exists
        query = select(GroupModel).where(GroupModel.id == group_id)
        if len(self.get_multi(query=query, session=session)) == 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Group not found.")
                
        try:
            # Update deleted_at for the group
            updated_group = group
            updated_group.deleted_at = datetime.now()

            # Update deleted_at for all members of the group
            stmt = (
                update(MemberModel)
                .where(
                    MemberModel.group_id == group_id,
                    MemberModel.deleted_at == None
                )
                .values(deleted_at=datetime.now())
            )
            session.exec(stmt)
            
            # Update the group
            self.update(obj_current=group, obj_new=updated_group, session=session)
            
            # Commit the changes
            session.commit()
                        
            return updated_group
        
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Something went wrong."
            )

group_controller = GroupController(GroupModel)