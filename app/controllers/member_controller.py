import uuid
from fastapi import HTTPException, status

from app.api.deps import SessionDep
from app.controllers.controller import Controller
from app.controllers.group_controller import group_controller
from app.models.member_model import MemberModel, MemberTypes
from app.resources.member_resource import MemberPublic
from app.models.group_model import GroupTypes
from sqlmodel import select


class MemberController(Controller[MemberModel, MemberModel, MemberModel]):

    def create_member(self, user_id: uuid.UUID, group_id: uuid.UUID, session: SessionDep) -> MemberPublic:
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
            member = MemberModel(user_id=user_id, group_id=group_id, role=MemberTypes.member)
            self.create(obj_in=member, session=session)

            group.member_count = group.member_count + 1
            session.commit()

            return MemberPublic(**member.__dict__)
        except:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong.")



member_controller = MemberController(MemberModel)
