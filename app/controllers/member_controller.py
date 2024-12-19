import uuid
from fastapi import HTTPException, status
from app.controllers.controller import Controller
from app.controllers.group_controller import group_controller
from app.models.member_model import MemberModel
from app.resources.member_resource import MemberPublic
from app.models.group_model import GroupTypes
from sqlmodel import select
from datetime import datetime


class MemberController(Controller[MemberModel, MemberModel, MemberModel]):
    
    def create_member(self, user_id: uuid.UUID, group_id: uuid.UUID) -> MemberPublic:
        group = group_controller.get(id=group_id)

        if group.type != GroupTypes.public_open:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to join.")
        
        query = select(MemberModel).where(MemberModel.user_id == user_id).where(MemberModel.group_id == group_id).where(MemberModel.deleted_at == None)
       
        if len(self.get_multi(query=query)) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already member of group.")
        
        try:
            member = MemberModel(user_id=user_id, group_id=group_id)
            member = self.create(obj_in=member)

            group.member_count = group.member_count + 1
            self.db_session.commit()
            
            return member
        except:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong.")



    def member_leave(self, user_id: uuid.UUID, group_id: uuid.UUID) -> MemberPublic:
        group = group_controller.get(id=group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found.")

        query = select(MemberModel).where(
            MemberModel.user_id == user_id,
            MemberModel.group_id == group_id
        )
        result = self.get_multi(query=query)
        member = result[0] if result else None
        
        if member is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not a member of the group.")
        
        if group.owner_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The owner cannot leave the group."
            )         

        if member.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="You already left the group."
            )        
        
        try:
            update_group_data = {"member_count": group.member_count - 1, "updated_at": datetime.now()}
            update_member_data = {"deleted_at": datetime.now(), "updated_at": datetime.now()}
            self.update(obj_current=member, obj_new=update_member_data)
            group_controller.update(obj_current=group, obj_new=update_group_data)
            self.db_session.commit()

            return member

        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong: {str(e)}"
            )

member_controller = MemberController(MemberModel)
