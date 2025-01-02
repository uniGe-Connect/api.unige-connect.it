import uuid
from app.controllers.controller import Controller
from app.models.group_model import GroupModel, GroupRequest
from app.models.member_model import MemberModel
from app.resources.group_resource import GroupPublic
from app.api.deps import SessionDep
from datetime import datetime
from sqlalchemy import select
from fastapi import HTTPException, status

class GroupController(Controller[GroupModel, GroupRequest, GroupModel]):

    def delete_group(self, group: GroupModel, group_id: uuid.UUID, session: SessionDep) -> GroupPublic:
        # Check if group exists
        query = select(GroupModel).where(GroupModel.id == group_id).where(GroupModel.id == group_id)
        if len(self.get_multi(query=query, session=session)) == 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Group not found.")
        
        try:
            # Update deleted_at
            updated_group = group
            updated_group.deleted_at = datetime.now()

            # Update deleted_at column of members of the group

            query = (
                select(MemberModel)
                .where(MemberModel.group_id == group_id and MemberModel.deleted_at == None)
            )
    
            members_public = self.get_multi(query=query, session=session)
            
            members_public_updated = members_public
            for member in members_public_updated:
                member.deleted_at = datetime.now()
                
            self.update(obj_current=members_public, obj_new=members_public_updated, session=session)
            self.update(obj_current=group, obj_new=updated_group, session=session)
                        
            return GroupPublic(data=updated_group)
        
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong.")

group_controller = GroupController(GroupModel)
