import uuid
from fastapi import HTTPException, status

from app.api.deps import SessionDep
from app.controllers.controller import Controller
from app.controllers.group_controller import group_controller
from app.models.user_model import UserModel
from app.models.member_model import MemberModel, MemberTypes
from app.resources.member_resource import MemberPublic
from app.resources.user_resource import UsersMemberPublic
from app.models.group_model import GroupTypes
from app.models.member_model import MemberTypes
from sqlmodel import select
from datetime import datetime


class MemberController(Controller[MemberModel, MemberModel, MemberModel]):

    def create_member(self, user_id: uuid.UUID, group_id: uuid.UUID, session: SessionDep, role: MemberTypes = MemberTypes.member) -> MemberPublic:
        group = group_controller.get(id=group_id, session=session)

        if group.type != GroupTypes.public_open:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to join.")

        query = (select(MemberModel)
            .where(MemberModel.user_id == user_id)
            .where(MemberModel.group_id == group_id)
            .where(MemberModel.deleted_at == None))

        if len(self.get_multi(query=query, session=session)) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already member of group.")

        try:
            member = MemberModel(user_id=user_id, group_id=group_id, role=role)
            self.create(obj_in=member, session=session)

            group.member_count = group.member_count + 1
            session.commit()

            return MemberPublic(**member.__dict__)
        except:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong.")
        
        
    def get_members(self, user_id: uuid.UUID, group_id: uuid.UUID, session: SessionDep) -> UsersMemberPublic:
        group = group_controller.get(id=group_id, session=session)

        query = select(MemberModel).where(MemberModel.user_id == user_id).where(MemberModel.group_id == group_id).where(MemberModel.deleted_at == None)
        if len(self.get_multi(query=query, session=session)) == 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a member of group.")
        
        try:
            # query = (
            #     select(UserModel.name, UserModel.last_name, MemberModel.role)
            #     .join(MemberModel, UserModel.id == MemberModel.user_id)
            #     .where(MemberModel.group_id == group_id)
            # )
            
            # members_public = self.get_multi(query=query, session=session)
            # filter out deleted members
            members_public = [member for member in group.users if member.deleted_at == None]
            
            return UsersMemberPublic(data=members_public, count=group.member_count)
        
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong.")
        
    def member_leave(self, user_id: uuid.UUID, group_id: uuid.UUID, session: SessionDep) -> MemberPublic:
        group = group_controller.get(id=group_id, session=session)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found.")

        query = select(MemberModel).where(
            MemberModel.user_id == user_id,
            MemberModel.group_id == group_id
        )
        result = self.get_multi(query=query, session=session)
        member = result[0] if result else None
        
        if member is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not a member of the group.")
        
        if group.owner_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The owner cannot leave the group."
            )         

        if member.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="You are not a member of the group anymore."
            )        
        
        try:
            update_group_data = {"member_count": group.member_count - 1, "updated_at": datetime.now()}
            update_member_data = {"deleted_at": datetime.now(), "updated_at": datetime.now()}
            self.update(obj_current=member, obj_new=update_member_data,  session=session)
            group_controller.update(obj_current=group, obj_new=update_group_data, session=session)
            session.commit()

            return member

        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong: {str(e)}"
            )

member_controller = MemberController(MemberModel)
